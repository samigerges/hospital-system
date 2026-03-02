# devices/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils import timezone

def create_sample_data(sender, **kwargs):
    from .models import Department, Device, Maintenance
    
    if not Department.objects.exists():
        departments = [
            Department(name='ICU', floor=3, phone='1234'),
            Department(name='Emergency', floor=1, phone='5678'),
            Department(name='Radiology', floor=2, phone='9012'),
            Department(name='Laboratory', floor=2, phone='3456'),
            Department(name='Outpatient Clinics', floor=1, phone='7890'),
        ]
        for dept in departments:
            dept.save()
        print("✅ Sample departments created")

class DevicesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'devices'
    verbose_name = 'Medical Equipment Management'
    
    def ready(self):
        post_migrate.connect(create_sample_data, sender=self)