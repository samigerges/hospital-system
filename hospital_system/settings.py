# hospital_system/settings.py
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS مع تحديث للـ IP الجديد
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "192.168.1.11",  # IP الجديد
]

# QR Codes للهوتسبوت
HOTSPOT_IP = '192.168.137.1'
HOTSPOT_URL = f'http://{HOTSPOT_IP}:8000'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Local apps
    'devices',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # For language switching
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospital_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'devices.context_processors.base_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'hospital_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# =====================

# Language settings
LANGUAGE_CODE = 'en-us'  # Default language

# Available languages
LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

# Locale paths for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Time zone for Egypt
TIME_ZONE = 'Africa/Cairo'

# Internationalization settings
USE_I18N = True     # Enable internationalization
USE_L10N = False    # Disable localization (we'll use custom formats)
USE_TZ = True       # Enable timezone support

# Date and time formats (English formats)
DATE_FORMAT = 'F j, Y'                # December 15, 2024
DATETIME_FORMAT = 'F j, Y H:i'        # December 15, 2024 14:30
SHORT_DATE_FORMAT = 'm/d/Y'           # 12/15/2024
SHORT_DATETIME_FORMAT = 'm/d/Y H:i'   # 12/15/2024 14:30
TIME_FORMAT = 'H:i'                   # 14:30
YEAR_MONTH_FORMAT = 'F Y'             # December 2024
MONTH_DAY_FORMAT = 'F j'              # December 15

# Number formatting
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','
DECIMAL_SEPARATOR = '.'
NUMBER_GROUPING = 3

# For Arabic RTL support
LANGUAGES_BIDI = ["ar"]

# Custom format module
FORMAT_MODULE_PATH = 'hospital_system.formats'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# إعدادات IP و BASE URL المحدثة
# ============================================

def get_local_ip():
    """Get local IP address"""
    try:
        # Try to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

# IP الحالي
LOCAL_IP = '192.168.1.11'  # قمت بتعيينه يدوياً بناءً على طلبك

# BASE URL الجديد - هذا هو الرابط الذي سيتم استخدامه في QR codes
BASE_URL = f'http://{LOCAL_IP}:8000'

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Authentication URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Admin language code (force English in admin)
ADMIN_LANGUAGE_CODE = 'en-us'

# Session settings (for language preference)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks in seconds
SESSION_SAVE_EVERY_REQUEST = True

# ============================================
# إعدادات إضافية للتعامل مع QR Codes
# ============================================

# إعدادات خاصة بـ QR Codes
QR_CODE_DIR = MEDIA_ROOT / 'qr_codes'
QR_CODE_URL = f'{BASE_URL}/media/qr_codes/'

# تأكد من إنشاء مجلد QR codes إذا لم يكن موجوداً
os.makedirs(QR_CODE_DIR, exist_ok=True)

# Security settings (for production, you should configure these)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
else:
    # Development settings
    INTERNAL_IPS = ['127.0.0.1']