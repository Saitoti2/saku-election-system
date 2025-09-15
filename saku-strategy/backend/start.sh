#!/bin/bash

# Navigate to the backend directory
cd saku-strategy/backend

# Set up the database properly
echo "Setting up database..."
python manage.py setup_database

# Start the application
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
