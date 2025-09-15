# 🚀 SAKU Election System - Google Cloud Deployment Guide

## 📋 **Deployment Summary**

✅ **Your SAKU Election System CAN run on Google Cloud Free Tier!**

### **System Analysis:**
- **Total Size**: 482MB (well under 5GB free storage)
- **Dependencies**: 82 Python packages (manageable)
- **Database**: 240KB SQLite (can migrate to Cloud SQL)
- **Expected Traffic**: Low to moderate (perfect for free tier)

## 🎯 **Recommended Deployment: Cloud Run**

### **Why Cloud Run?**
- ✅ **2M requests/month** (more than enough for university elections)
- ✅ **180K vCPU-seconds** (sufficient for your Django app)
- ✅ **Auto-scaling** (handles election day traffic spikes)
- ✅ **Pay-per-use** (costs nothing when not in use)
- ✅ **Easy deployment** (container-based)

## 📦 **Step-by-Step Deployment**

### **1. Prepare Your Application**

#### **Create Dockerfile:**
```dockerfile
# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Run the application
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 core.wsgi:application
```

#### **Create .dockerignore:**
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.venv
venv/
ENV/
env/
.env
```

### **2. Optimize for Cloud Run**

#### **Update settings.py for production:**
```python
# Add to your settings.py
import os

# Cloud Run specific settings
if os.getenv('GAE_ENV') or os.getenv('CLOUD_RUN'):
    # Use Cloud SQL or Firestore instead of SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'saku_election'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }
    
    # Use Cloud Storage for media files
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
    
    # Security settings
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### **3. Deploy to Cloud Run**

#### **Using gcloud CLI:**
```bash
# Build and deploy
gcloud run deploy saku-election-system \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars DEBUG=False,SECRET_KEY=your-secret-key
```

#### **Using Cloud Console:**
1. Go to Cloud Run in Google Cloud Console
2. Click "Create Service"
3. Choose "Deploy from source repository"
4. Connect your GitHub repository
5. Set build configuration
6. Deploy!

## 💰 **Cost Estimation**

### **Free Tier Usage (Monthly):**
- **Requests**: ~50K (well under 2M limit) ✅
- **Compute Time**: ~10K vCPU-seconds (well under 180K limit) ✅
- **Storage**: ~500MB (well under 5GB limit) ✅
- **Data Transfer**: ~1GB (within 1GB free limit) ✅

### **Expected Cost: $0/month** 🎉

## 🔧 **Optimization Tips**

### **1. Reduce Dependencies**
```bash
# Create minimal requirements.txt
pip freeze | grep -E "(Django|djangorestframework|gunicorn|whitenoise|psycopg2)" > requirements-minimal.txt
```

### **2. Use Cloud Storage for Documents**
- Move student document uploads to Cloud Storage
- Reduces container size and improves performance

### **3. Database Migration**
- Consider migrating from SQLite to Cloud SQL or Firestore
- Better for concurrent users and data persistence

### **4. Static File Optimization**
- Use WhiteNoise for static files
- Enable gzip compression
- Optimize images and CSS

## 🚨 **Important Notes**

### **Free Tier Limits:**
- **2M requests/month** - Monitor usage
- **180K vCPU-seconds** - Optimize cold starts
- **1GB outbound data** - Compress responses
- **5GB storage** - Clean up old files

### **Monitoring:**
- Set up Cloud Monitoring alerts
- Track resource usage
- Monitor costs

## 🎯 **Alternative Options**

### **If Cloud Run doesn't work:**

#### **App Engine Standard:**
- 28 frontend instance hours/day free
- Automatic scaling
- Easy deployment

#### **Compute Engine (e2-micro):**
- 1 instance/month free
- 30GB disk storage
- Always-on but limited resources

## ✅ **Final Recommendation**

**Deploy on Cloud Run** - It's the perfect fit for your SAKU Election System:

1. **Cost-effective**: Free tier covers your needs
2. **Scalable**: Handles election day traffic
3. **Modern**: Serverless architecture
4. **Easy**: Simple deployment process
5. **Reliable**: Google's managed infrastructure

Your system will run smoothly on Google Cloud Free Tier! 🚀
