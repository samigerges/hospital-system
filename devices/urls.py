# devices/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ============================================
    # AUTHENTICATION URLs (المصادقة)
    # ============================================
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ============================================
    # DASHBOARD & CONTROL CENTER URLs (لوحات التحكم)
    # ============================================
    path('', views.control_center, name='control_center'),  # الصفحة الرئيسية (بدون slash)
    path('control-center/', views.control_center, name='control_center_dash'),  # مع dash
    
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard التقليدي
    
    # ============================================
    # TEAM PROFILE URL (ملف الفريق) - أضف هذا السطر
    # ============================================
    path('team-profile/', views.team_profile, name='team_profile'),
    
    # ============================================
    # DEVICES MANAGEMENT URLs (إدارة الأجهزة)
    # ============================================
    # قائمة الأجهزة
    path('devices/', views.device_list, name='device_list'),
    
    # إضافة جهاز جديد
    path('devices/add/', views.device_add, name='device_add'),
    
    # تفاصيل الجهاز (تعمل مع المستخدمين المسجلين والزوار)
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    
    # تعديل جهاز
    path('devices/<int:pk>/edit/', views.device_edit, name='device_edit'),
    
    # حذف جهاز
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),
    
    # توليد QR Code للجهاز
    path('devices/<int:pk>/generate-qr/', views.generate_device_qr, name='generate_device_qr'),
    
    # ============================================
    # DEPARTMENTS MANAGEMENT URLs (إدارة الأقسام)
    # ============================================
    # قائمة الأقسام
    path('departments/', views.departments_list, name='departments_list'),
    
    # إضافة قسم جديد
    path('departments/add/', views.department_add, name='department_add'),
    
    # تعديل قسم
    path('departments/<int:pk>/edit/', views.department_edit, name='department_edit'),
    
    # حذف قسم
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    

    path('procurement/', views.procurement_dashboard, name='procurement_dashboard'),
    path('technician/', views.technician_workbench, name='technician_workbench'),
    path('technician/scan/', views.technician_device_from_qr, name='technician_device_from_qr'),
    path('technician/device/<int:pk>/', views.technician_device, name='technician_device'),
    path('technician/device/<int:pk>/start-work-order/', views.technician_start_work_order, name='technician_start_work_order'),
    path('technician/work-order/<int:maintenance_id>/stop/', views.technician_stop_work_order, name='technician_stop_work_order'),
    path('technician/work-order/<int:maintenance_id>/sync-notes/', views.technician_sync_notes, name='technician_sync_notes'),

    # ============================================
    # REPORTS URLs (التقارير)
    # ============================================
    path('reports/', views.reports_view, name='reports'),
    
    # ============================================
    # EXPORT URLs (التصدير)
    # ============================================
    path('devices/export/excel/', views.devices_export_excel, name='devices_export_excel'),
    
    # ============================================
    # API ENDPOINTS (واجهات برمجية)
    # ============================================
    # API لإحصائيات Control Center (للتحديث التلقائي)
    path('control-center/api/stats/', views.control_center_stats_api, name='control_center_stats_api'),
    
    # API للبحث السريع عن جهاز
    path('devices/api/lookup/', views.device_lookup_api, name='device_lookup_api'),
    path('maintenance/api/calendar/', views.maintenance_calendar_api, name='maintenance_calendar_api'),
    
    # URL لعرض QR Code كصورة
    path('devices/<int:pk>/qr.png', views.device_qr, name='device_qr'),
]