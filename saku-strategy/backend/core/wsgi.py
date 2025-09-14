"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use Railway settings if DATABASE_URL is present (Railway deployment)
if os.getenv('DATABASE_URL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.railway_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
