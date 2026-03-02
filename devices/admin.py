# devices/admin.py
from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Device, Department, Maintenance

@admin.action(description="Add sample data")
def create_sample_data(modeladmin, request, queryset):
    try:
        departments = [
            Department(name='ICU', floor=3, phone='1234'),
            Department(name='Emergency', floor=1, phone='5678'),
            Department(name='Radiology', floor=2, phone='9012'),
            Department(name='Laboratory', floor=2, phone='3456'),
        ]
        
        for dept in departments:
            if not Department.objects.filter(name=dept.name).exists():
                dept.save()
        
        devices_data = [
            {
                'name': 'Patient Monitor',
                'device_id': 'MON-001',
                'serial_number': 'SN-1001',
                'device_type': 'monitor',
                'manufacturer': 'Philips',
                'model': 'IntelliVue MX450',
                'status': 'active',
                'price': 25000,
            },
            {
                'name': 'Smart Infusion Pump',
                'device_id': 'INF-001',
                'serial_number': 'SN-1002',
                'device_type': 'infusion_pump',
                'manufacturer': 'Baxter',
                'model': 'Sigma Spectrum',
                'status': 'active',
                'price': 18000,
            },
            {
                'name': 'Ventilator',
                'device_id': 'VEN-001',
                'serial_number': 'SN-1003',
                'device_type': 'ventilator',
                'manufacturer': 'Dräger',
                'model': 'Evita V600',
                'status': 'maintenance',
                'price': 45000,
            },
        ]
        
        for device_data in devices_data:
            if not Device.objects.filter(device_id=device_data['device_id']).exists():
                device = Device(**device_data)
                device.purchase_date = timezone.now().date() - timedelta(days=365)
                device.warranty_expiry = timezone.now().date() + timedelta(days=180)
                device.location = 'ICU'
                device.save()
        
        messages.success(request, "✅ Sample data created successfully!")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 1
    fields = ['maintenance_type', 'date', 'technician', 'assigned_technician', 'status', 'sla_deadline', 'cost', 'completed']

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'name', 'device_type', 'status', 'department', 'location']
    list_filter = ['status', 'device_type', 'department']
    search_fields = ['device_id', 'name', 'serial_number']
    readonly_fields = ['qr_code', 'created_at', 'updated_at']
    inlines = [MaintenanceInline]
    actions = [create_sample_data]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'floor', 'phone', 'device_count']
    search_fields = ['name']
    
    def device_count(self, obj):
        return obj.device_set.count()
    device_count.short_description = 'Device Count'

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['device', 'maintenance_type', 'date', 'technician', 'assigned_technician', 'status', 'sla_deadline', 'sla_breached', 'cost', 'completed']
    list_filter = ['maintenance_type', 'status', 'completed', 'date']
    search_fields = ['device__name', 'technician', 'assigned_technician']

    def sla_breached(self, obj):
        return obj.is_sla_breached
    sla_breached.boolean = True
    sla_breached.short_description = 'SLA Breached'

admin.site.site_header = "Hospital Equipment Management System"
admin.site.site_title = "Equipment Management"
admin.site.index_title = "Welcome to Control Panel"
