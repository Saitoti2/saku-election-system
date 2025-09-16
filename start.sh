#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "🚀 Starting SAKU Election System deployment..."

# Set up the database
echo "📊 Setting up database..."
python manage.py migrate || echo "⚠️ Migration failed, continuing..."

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
python manage.py shell << 'PYTHON_EOF'
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('✅ Superuser created: admin/admin123')
    else:
        print('✅ Superuser already exists')
except Exception as e:
    print(f'⚠️ Superuser creation failed: {e}')
PYTHON_EOF

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "⚠️ collectstatic failed, continuing..."

# Start the application
echo "🌐 Starting Gunicorn server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 300
