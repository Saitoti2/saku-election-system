#!/usr/bin/env python
"""
Simple Flask-like app for Railway deployment
"""
import os
import sys
import django
from django.core.wsgi import get_wsgi_application

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
django.setup()

# Get the WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    # For local development
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)