#!/bin/bash

# Navigate to the backend directory
cd saku-strategy/backend

# Run the deployment script
echo "Running deployment setup..."
python deploy.py

# Start the application
echo "Starting Gunicorn..."
exec gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
