from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import Department, Device, Maintenance


class MaintenanceWorkOrderTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='ICU', floor=1)
        self.device = Device.objects.create(
            name='Monitor',
            device_id='MON-100',
            serial_number='SER-100',
            device_type='monitor',
            manufacturer='Acme',
            model='A1',
            purchase_date=timezone.now().date(),
            warranty_expiry=timezone.now().date() + timedelta(days=365),
            price='1000.00',
            status='active',
            department=self.department,
            location='Room 1',
        )

    def test_completed_flag_tracks_status(self):
        maintenance = Maintenance.objects.create(
            device=self.device,
            maintenance_type='corrective',
            technician='Tech 1',
            assigned_technician='Tech 2',
            description='Fix issue',
            status='in_progress',
        )
        self.assertFalse(maintenance.completed)

        maintenance.status = 'completed'
        maintenance.save()
        self.assertTrue(maintenance.completed)

    def test_status_cannot_move_backwards(self):
        maintenance = Maintenance.objects.create(
            device=self.device,
            maintenance_type='corrective',
            technician='Tech 1',
            assigned_technician='Tech 2',
            description='Fix issue',
            status='in_progress',
        )

        maintenance.status = 'assigned'
        with self.assertRaises(ValidationError):
            maintenance.save()

    def test_sla_breach_indicator(self):
        maintenance = Maintenance.objects.create(
            device=self.device,
            maintenance_type='preventive',
            technician='Tech 1',
            assigned_technician='Tech 2',
            description='Routine',
            status='assigned',
            sla_deadline=timezone.now() - timedelta(hours=2),
        )
        self.assertTrue(maintenance.is_sla_breached)

        maintenance.status = 'verified'
        maintenance.save()
        self.assertFalse(maintenance.is_sla_breached)
