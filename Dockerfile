# Dockerfile for SAKU Election System
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set working directory to backend
WORKDIR /app/saku-strategy/backend

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start command
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
