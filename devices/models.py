# devices/models.py
from django.core.exceptions import ValidationError
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Department Name')
    floor = models.IntegerField(verbose_name='Floor')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Phone Number')
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
    
    def __str__(self):
        return f"{self.name} - Floor {self.floor}"

class Device(models.Model):
    DEVICE_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]
    
    DEVICE_TYPE = [
        ('monitor', 'Monitor'),
        ('infusion_pump', 'Infusion Pump'),
        ('ventilator', 'Ventilator'),
        ('defibrillator', 'Defibrillator'),
        ('ultrasound', 'Ultrasound'),
        ('xray', 'X-Ray'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Device Name')
    device_id = models.CharField(max_length=50, unique=True, verbose_name='Device ID')
    serial_number = models.CharField(max_length=100, unique=True, verbose_name='Serial Number')
    device_type = models.CharField(max_length=50, choices=DEVICE_TYPE, verbose_name='Device Type')
    manufacturer = models.CharField(max_length=200, verbose_name='Manufacturer')
    model = models.CharField(max_length=200, verbose_name='Model')
    purchase_date = models.DateField(verbose_name='Purchase Date')
    warranty_expiry = models.DateField(verbose_name='Warranty Expiry')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    status = models.CharField(max_length=20, choices=DEVICE_STATUS, default='active', verbose_name='Status')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Department')
    location = models.CharField(max_length=200, verbose_name='Location')
    last_maintenance = models.DateField(null=True, blank=True, verbose_name='Last Maintenance')
    next_maintenance = models.DateField(null=True, blank=True, verbose_name='Next Maintenance')
    notes = models.TextField(blank=True, verbose_name='Notes')
    qr_code = models.ImageField(blank=True, upload_to='qrcodes/', verbose_name='QR Code')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        verbose_name = 'Device'
        verbose_name_plural = 'Devices'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.device_id})"
    
    def get_absolute_url(self):
        return reverse('device_detail', kwargs={'pk': self.pk})
    
    def get_status_color(self):
        colors = {
            'active': 'success',
            'inactive': 'secondary',
            'maintenance': 'warning',
            'retired': 'danger'
        }
        return colors.get(self.status, 'secondary')
    
    def generate_qr_code(self):
        device_url = settings.BASE_URL + self.get_absolute_url()
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(device_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        filename = f'qr_{self.device_id}_{self.id}.png'
        self.qr_code.save(filename, File(buffer), save=False)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_code:
            self.generate_qr_code()
            kwargs.pop('force_insert', None)
            super().save(*args, **kwargs)

class Maintenance(models.Model):
    MAINTENANCE_TYPE = [
        ('preventive', 'Preventive Maintenance'),
        ('corrective', 'Corrective Maintenance'),
        ('emergency', 'Emergency Maintenance'),
        ('calibration', 'Calibration'),
    ]

    WORK_ORDER_STATUS = [
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('waiting_parts', 'Waiting Parts'),
        ('completed', 'Completed'),
        ('verified', 'Verified'),
    ]

    STATUS_SEQUENCE = {
        'new': 0,
        'assigned': 1,
        'in_progress': 2,
        'waiting_parts': 3,
        'completed': 4,
        'verified': 5,
    }
    
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='maintenances', verbose_name='Device')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPE, verbose_name='Maintenance Type')
    date = models.DateField(default=timezone.now, verbose_name='Maintenance Date')
    technician = models.CharField(max_length=200, verbose_name='Technician')
    assigned_technician = models.CharField(max_length=200, blank=True, verbose_name='Assigned Technician')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Cost')
    description = models.TextField(verbose_name='Work Description')
    notes = models.TextField(blank=True, verbose_name='Notes')
    status = models.CharField(max_length=20, choices=WORK_ORDER_STATUS, default='new', verbose_name='Work Order Status')
    sla_deadline = models.DateTimeField(null=True, blank=True, verbose_name='SLA Deadline')
    photo_attachment = models.FileField(upload_to='maintenance/photos/', null=True, blank=True, verbose_name='Photo Attachment')
    calibration_certificate = models.FileField(upload_to='maintenance/calibration/', null=True, blank=True, verbose_name='Calibration Certificate')
    completed = models.BooleanField(default=True, verbose_name='Completed')
    next_maintenance_date = models.DateField(blank=True, null=True, verbose_name='Next Maintenance Date')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Maintenance'
        verbose_name_plural = 'Maintenance Records'
        ordering = ['-date']
    
    def __str__(self):
        return f"Maintenance {self.device.name} - {self.date}"

    @property
    def is_sla_breached(self):
        if not self.sla_deadline:
            return False
        return timezone.now() > self.sla_deadline and self.status not in {'completed', 'verified'}

    def clean(self):
        super().clean()
        if not self.pk:
            return

        previous = Maintenance.objects.filter(pk=self.pk).values_list('status', flat=True).first()
        if not previous:
            return

        if self.STATUS_SEQUENCE[self.status] < self.STATUS_SEQUENCE[previous]:
            raise ValidationError({'status': 'Status cannot move backwards in the work order flow.'})

    def save(self, *args, **kwargs):
        self.completed = self.status in {'completed', 'verified'}
        self.full_clean()
        super().save(*args, **kwargs)
