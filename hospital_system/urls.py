from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pathlib import Path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('devices.urls')),  # هذا يربط جميع روابط devices
]

if settings.DEBUG:
    # serve media files (media/qr_codes/*.png) and static files during development
    urlpatterns += static(settings.MEDIA_URL, document_root=str(settings.MEDIA_ROOT))
    # serve the project's static/ directory in DEBUG
    if settings.STATICFILES_DIRS:
        urlpatterns += static(settings.STATIC_URL, document_root=str(settings.STATICFILES_DIRS[0]))