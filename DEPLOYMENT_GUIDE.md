# SAKU Election System - Deployment Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click "New repository"
3. Repository name: `saku-election-system`
4. Description: `SAKU Election Management System - Student registration and verification platform`
5. Set to **Private** (recommended for sensitive data)
6. Click "Create repository"

## Step 2: Push to GitHub

Run these commands in your terminal:

```bash
cd "/Users/saitoti/SAKU ASSOCIATION STRATEGY APP"
git remote add origin https://github.com/YOUR_USERNAME/saku-election-system.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## Step 3: Deploy with Live Updates

### Option A: Railway (Recommended - Easy Setup)

1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `saku-election-system` repository
5. Railway will automatically detect Django and deploy

**Environment Variables to set in Railway:**
```
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app
ADMIN_PHONE_NUMBER=+254769582779
```

### Option B: Heroku (Alternative)

1. Go to [Heroku.com](https://heroku.com)
2. Create new app
3. Connect GitHub repository
4. Enable automatic deploys

### Option C: DigitalOcean App Platform

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Create new app from GitHub
3. Select your repository
4. Configure build and run commands

## Step 4: Configure Production Settings

Create a production settings file:

```python
# backend/core/production_settings.py
import os
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-app.railway.app']

# Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Step 5: Live Updates Setup

### Automatic Deployments
- **Railway/Heroku**: Automatically deploys when you push to main branch
- **GitHub Actions**: Set up CI/CD pipeline for custom deployment

### Manual Updates
```bash
# Make changes locally
git add .
git commit -m "Update feature X"
git push origin main

# Platform automatically deploys the changes
```

## Step 6: Domain Setup (Optional)

1. Buy a domain (e.g., `saku-elections.com`)
2. Configure DNS to point to your deployment platform
3. Update `ALLOWED_HOSTS` in production settings

## Step 7: SSL Certificate

Most platforms (Railway, Heroku, DigitalOcean) provide free SSL certificates automatically.

## Step 8: Database Migration

After deployment, run migrations:

```bash
# In your platform's console or via CLI
python manage.py migrate
python manage.py createsuperuser
```

## Step 9: Test Deployment

1. Visit your deployed URL
2. Test student signup
3. Test admin login
4. Verify all features work

## Monitoring and Maintenance

### Logs
- Check platform logs for errors
- Monitor performance metrics

### Updates
- Push changes to GitHub
- Platform automatically redeploys
- Zero-downtime deployments

### Backup
- Regular database backups
- Export user data periodically

## Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Use strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS
- [ ] Regular security updates
- [ ] Monitor access logs

## Support

For deployment issues:
1. Check platform documentation
2. Review error logs
3. Test locally first
4. Contact platform support

---

**Your SAKU Election System is now live and ready for students to register!** 🎉
