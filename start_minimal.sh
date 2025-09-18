#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

echo "🚀 Starting SAKU Election System deployment... [MINIMAL VERSION]"

# Debug: Check environment variables
echo "🔍 Environment check:"
echo "DATABASE_URL: $DATABASE_URL"
echo "PORT: $PORT"

# Set Django settings to minimal
export DJANGO_SETTINGS_MODULE=core.minimal_settings

# Set up the database
echo "📊 Setting up database..."
if python manage.py migrate --noinput; then
    echo "✅ Database migrations applied successfully."
else
    echo "❌ Database migrations failed. Continuing anyway..."
fi

# Create superuser if it doesn't exist
echo "👤 Creating superuser..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')"; then
    echo "✅ Superuser 'admin' ensured (created if not exists, password: admin123)."
else
    echo "⚠️ Superuser creation failed or already exists."
fi

# Collect static files
echo "📁 Collecting static files..."
if python manage.py collectstatic --noinput; then
    echo "✅ Static files collected successfully."
else
    echo "⚠️ Static files collection failed. Continuing without it."
fi

# Start the application
echo "🌐 Starting Gunicorn server..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
