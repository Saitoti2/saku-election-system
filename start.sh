#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "🚀 Starting SAKU Election System deployment..."

# Set up the database
echo "📊 Setting up database..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
EOF

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the application
echo "🌐 Starting Gunicorn server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120