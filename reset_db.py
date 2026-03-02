# reset_db.py
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_system.settings')
django.setup()

from django.core.management import execute_from_command_line
from devices.models import Department, Device, Maintenance
from django.utils import timezone
from datetime import timedelta

def reset_database():
    print("🔄 Deleting database...")
    
    Device.objects.all().delete()
    Department.objects.all().delete()
    Maintenance.objects.all().delete()
    
    print("✅ All data deleted")
    print("🔄 Adding sample data...")
    
    departments = [
        Department(name='ICU', floor=3, phone='1234'),
        Department(name='Emergency', floor=1, phone='5678'),
        Department(name='Radiology', floor=2, phone='9012'),
        Department(name='Laboratory', floor=2, phone='3456'),
        Department(name='Outpatient Clinics', floor=1, phone='7890'),
    ]
    
    for dept in departments:
        dept.save()
    
    print(f"✅ Created {len(departments)} departments")
    
    devices_data = [
        {
            'name': 'Advanced Patient Monitor',
            'device_id': 'MON-001',
            'serial_number': 'SN-1001',
            'device_type': 'monitor',
            'manufacturer': 'Philips',
            'model': 'IntelliVue MX450',
            'status': 'active',
            'price': 25000,
            'department': departments[0],
            'location': 'Bed 1 - ICU',
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
            'department': departments[1],
            'location': 'Emergency Room 2',
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
            'department': departments[0],
            'location': 'ICU - Respiratory Unit',
        },
        {
            'name': 'Defibrillator',
            'device_id': 'DEF-001',
            'serial_number': 'SN-1004',
            'device_type': 'defibrillator',
            'manufacturer': 'Zoll',
            'model': 'X Series',
            'status': 'active',
            'price': 32000,
            'department': departments[1],
            'location': 'Emergency Cart',
        },
        {
            'name': 'CT Scanner',
            'device_id': 'XRY-001',
            'serial_number': 'SN-1005',
            'device_type': 'xray',
            'manufacturer': 'Siemens',
            'model': 'SOMATOM',
            'status': 'active',
            'price': 1200000,
            'department': departments[2],
            'location': 'Radiology Department',
        },
    ]
    
    created_devices = []
    for device_data in devices_data:
        device = Device(**device_data)
        device.purchase_date = timezone.now().date() - timedelta(days=365)
        device.warranty_expiry = timezone.now().date() + timedelta(days=180)
        device.last_maintenance = timezone.now().date() - timedelta(days=30)
        device.next_maintenance = timezone.now().date() + timedelta(days=90)
        device.notes = "High quality device - requires regular maintenance"
        device.save()
        created_devices.append(device)
    
    print(f"✅ Created {len(created_devices)} devices")
    
    maintenance_data = [
        {
            'device': created_devices[2],
            'maintenance_type': 'preventive',
            'date': timezone.now().date() - timedelta(days=30),
            'technician': 'Ahmed Mohamed',
            'cost': 1500,
            'description': 'Routine maintenance - filter change - cleaning',
            'completed': True,
        },
        {
            'device': created_devices[0],
            'maintenance_type': 'corrective',
            'date': timezone.now().date() - timedelta(days=15),
            'technician': 'Mostafa Ali',
            'cost': 800,
            'description': 'Display screen repair - cable replacement',
            'completed': True,
        },
    ]
    
    for maint_data in maintenance_data:
        Maintenance.objects.create(**maint_data)
    
    print(f"✅ Created maintenance records")
    print("\n🎉 Database reset successfully!")
    print("📊 Available data:")
    print(f"   - {Department.objects.count()} departments")
    print(f"   - {Device.objects.count()} devices")
    print(f"   - {Maintenance.objects.count()} maintenance records")
    print("\n🔑 Login using your admin credentials")
    print("🌐 Open http://127.0.0.1:8000/ to start")

if __name__ == '__main__':
    confirm = input("Are you sure you want to reset the database? (yes/no): ")
    if confirm.lower() in ['yes', 'y']:
        reset_database()
    else:
        print("❌ Operation cancelled")