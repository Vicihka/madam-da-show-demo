"""
Production Settings for MADAM DA E-Commerce Platform

DO NOT use this file directly in production!
Instead, set environment variables and use settings.py with DEBUG=False.

This file serves as a reference for production configuration.
"""

from .settings import *
import os

# ============================================================================
# CRITICAL PRODUCTION SETTINGS
# ============================================================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# MUST be set via environment variable: SECRET_KEY
if not SECRET_KEY or SECRET_KEY == 'django-insecure-wr-e*gp=1*s26id!o2h#tik($w^#olr20*8wn98aplo#wma%!u':
    raise ValueError("SECRET_KEY must be set in production environment!")

# ALLOWED_HOSTS: MUST be set via environment variable
# Example: ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '').strip()
if not allowed_hosts_env:
    raise ValueError("ALLOWED_HOSTS must be set in production environment!")
ALLOWED_HOSTS = [host.strip() for host in allowed_hosts_env.split(',') if host.strip()]

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Use PostgreSQL in production (configured via environment variables)
# Required environment variables:
# - DATABASE_URL (preferred, uses dj-database-url)
# OR
# - DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Connection pooling is enabled by default
# CONN_MAX_AGE = 600 (10 minutes)

# ============================================================================
# SECURITY SETTINGS
# ============================================================================

# HTTPS Settings (enable if behind a proxy/load balancer with SSL)
ENABLE_SSL_REDIRECT = os.environ.get('ENABLE_SSL_REDIRECT', 'False').lower() == 'true'
if ENABLE_SSL_REDIRECT:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    SECURE_SSL_REDIRECT = False

# CSRF Settings
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True  # HTTPS only in production
CSRF_TRUSTED_ORIGINS = [
    host for host in ALLOWED_HOSTS 
    if host.startswith('https://') or host.startswith('http://')
] + [origin.strip() for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if origin.strip()]

# Session Settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = True  # HTTPS only in production
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# Security Headers (already set in settings.py, but ensure they're enabled)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Proxy Settings (if behind a reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ============================================================================
# CACHING & PERFORMANCE
# ============================================================================

# Use Redis for caching in production
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1')

try:
    import django_redis
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
                'IGNORE_EXCEPTIONS': True,  # Don't crash if Redis is down
            },
            'KEY_PREFIX': 'madamda',
            'TIMEOUT': 300,  # 5 minutes default
        }
    }
    # Use cache for sessions
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'default'
except ImportError:
    # Fallback to Redis cache backend (Django 4.0+)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
        }
    }

# ============================================================================
# STATIC FILES & MEDIA
# ============================================================================

# Static files are served by WhiteNoise in production
# Run: python manage.py collectstatic before deployment
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (product images, QR codes, etc.)
# Consider using cloud storage (S3, Cloudinary, etc.) for production
MEDIA_ROOT = BASE_DIR / 'media'
# Or use cloud storage:
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# ============================================================================
# LOGGING
# ============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'security': {
            'format': 'SECURITY {asctime} {levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'formatter': 'security',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        # Add email handler for critical errors (optional)
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'include_html': True,
        # },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'app': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Create logs directory if it doesn't exist
logs_dir = BASE_DIR / 'logs'
if not logs_dir.exists():
    os.makedirs(logs_dir, exist_ok=True)

# ============================================================================
# EMAIL CONFIGURATION (if needed)
# ============================================================================

# Configure email backend for production
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@yourdomain.com')

# ============================================================================
# EXTERNAL SERVICES
# ============================================================================

# Bakong Payment API
BAKONG_API_BASE = os.environ.get('BAKONG_API_BASE', 'https://bakongapi.com')
BAKONG_ID = os.environ.get('BAKONG_ID', '')
BAKONG_MERCHANT_NAME = os.environ.get('BAKONG_MERCHANT_NAME', 'MADAM DA')

if not BAKONG_ID:
    # Log warning but don't crash (payment won't work)
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("BAKONG_ID not set - payment processing will not work")

# Telegram Bot (for order notifications)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')
TELEGRAM_ENABLED = bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

# ============================================================================
# PERFORMANCE OPTIMIZATIONS
# ============================================================================

# Database connection pooling
DATABASES['default']['CONN_MAX_AGE'] = 600  # 10 minutes

# Disable atomic requests for better performance
# Use @transaction.atomic in views that need transactions
DATABASES['default']['ATOMIC_REQUESTS'] = False

# ============================================================================
# ADMIN SECURITY
# ============================================================================

# Change admin URL for security (set via environment variable)
ADMIN_URL = os.environ.get('ADMIN_URL', 'admin/')

# Optional: IP whitelist for admin (configure in middleware)
# Set ADMIN_IP_WHITELIST environment variable (comma-separated IPs)

# ============================================================================
# CORS SETTINGS (if API is accessed from frontend)
# ============================================================================

CORS_ALLOWED_ORIGINS = [
    origin.strip() for origin in os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ['GET', 'POST', 'OPTIONS']
CORS_ALLOW_HEADERS = ['Content-Type', 'X-CSRFToken']

# ============================================================================
# RATE LIMITING
# ============================================================================

RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'

# ============================================================================
# FILE UPLOAD LIMITS
# ============================================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# ============================================================================
# CHANNEL LAYERS (WebSocket)
# ============================================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [REDIS_URL.replace('redis://', '').split('/')[0].split(':')] if REDIS_URL else [('127.0.0.1', 6379)],
        },
    },
}

# ============================================================================
# PRODUCTION-SPECIFIC MIDDLEWARE
# ============================================================================

# Ensure WhiteNoise is enabled for static files
# Already in MIDDLEWARE: 'whitenoise.middleware.WhiteNoiseMiddleware'

# ============================================================================
# VALIDATION
# ============================================================================

# Ensure critical settings are set
assert not DEBUG, "DEBUG must be False in production!"
assert SECRET_KEY and SECRET_KEY != 'django-insecure-*', "SECRET_KEY must be set!"
assert ALLOWED_HOSTS, "ALLOWED_HOSTS must be set!"

print("✅ Production settings loaded successfully")
print(f"   ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"   DEBUG: {DEBUG}")
print(f"   Database: {DATABASES['default'].get('ENGINE', 'Unknown')}")
