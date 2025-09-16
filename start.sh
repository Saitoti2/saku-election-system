#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "🚀 Starting SAKU Election System deployment..."

# Debug: Check if files exist
echo "🔍 Debugging file structure..."
ls -la
echo "📁 Core directory:"
ls -la core/
echo "📁 Elections directory:"
ls -la elections/

# Test Django settings
echo "�� Testing Django settings..."
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.conf import settings
print('✅ ROOT_URLCONF:', getattr(settings, 'ROOT_URLCONF', 'NOT FOUND'))
print('✅ INSTALLED_APPS count:', len(settings.INSTALLED_APPS))
"

# Set up the database
echo "📊 Setting up database..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell << 'PYTHON_EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
PYTHON_EOF

# Collect static files (skip if command not found)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "⚠️ collectstatic command not found, skipping..."

# Start the application
echo "🌐 Starting Gunicorn server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 300
