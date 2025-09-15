"""
WSGI entry point for Render deployment.
This file redirects to the Django WSGI application.
"""

import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'saku-strategy', 'backend'))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Import and expose the Django WSGI application
from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
