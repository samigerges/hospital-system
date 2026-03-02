
# devices/context_processors.py
from django.conf import settings

def base_url(request):
    return {
        'BASE_URL': settings.BASE_URL,
    }