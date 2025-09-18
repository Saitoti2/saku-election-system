# Production settings for Railway deployment
import os
import dj_database_url
from .settings import *

# Security settings for production
DEBUG = False
ALLOWED_HOSTS = ['*']  # Railway will set this automatically

# SSL/Security settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Database configuration for Railway - EXPLICIT AND BULLETPROOF
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

print(f"🔍 Production Database URL: {DATABASE_URL}")

# Explicit database configuration - no dj_database_url dependency
if DATABASE_URL.startswith('postgresql://'):
    # Parse PostgreSQL URL manually
    import urllib.parse as urlparse
    url = urlparse.urlparse(DATABASE_URL)
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': url.path[1:],  # Remove leading slash
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port or 5432,
        }
    }
else:
    # SQLite fallback
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

print(f"🔍 Production Database ENGINE: {DATABASES['default'].get('ENGINE', 'NOT SET')}")
print(f"🔍 Production Database NAME: {DATABASES['default'].get('NAME', 'NOT SET')}")

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}