#!/bin/bash

# Navigate to the backend directory
cd saku-strategy/backend

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create a superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created: username=admin, password=admin123")
else:
    print("Superuser already exists")
EOF

# Start the application
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
