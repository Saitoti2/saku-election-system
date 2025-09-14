"""
Railway-specific Django settings for production deployment
"""
import os
import dj_database_url
from .settings import *

# Production settings for Railway
DEBUG = False

# Security
SECRET_KEY = os.getenv('SECRET_KEY', 'railway-production-secret-key-change-this')
ALLOWED_HOSTS = ['*']  # Railway will provide the actual domain

# Database - Railway provides DATABASE_URL automatically
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

# Static files configuration for Railway
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise for static files serving
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings for Railway
CORS_ALLOWED_ORIGINS = [
    "https://*.railway.app",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Admin phone number for WhatsApp notifications
ADMIN_PHONE_NUMBER = os.getenv('ADMIN_PHONE_NUMBER', '+254769582779')

# Logging configuration for Railway
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Gunicorn configuration
# These settings are applied when running with Gunicorn
import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
