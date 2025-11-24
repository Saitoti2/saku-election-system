# SAKU Election System - Deployment Guide

This guide will help you deploy the SAKU Election System backend to Render and frontend to Vercel.

## Table of Contents
1. [Backend Deployment (Render)](#backend-deployment-render)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Environment Variables](#environment-variables)
4. [Post-Deployment Configuration](#post-deployment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## Backend Deployment (Render)

### Step 1: Prepare Your Repository
1. Ensure all changes are committed and pushed to your Git repository
2. Make sure `requirements.txt` and `Procfile` are in the root directory

### Step 2: Create a Render Web Service
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your Git repository
4. Configure the service:
   - **Name**: `saku-election-backend` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: Leave empty (root of repo)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`

### Step 3: Set Environment Variables in Render
Go to your service → **Environment** tab and add:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here-generate-a-random-one
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com,localhost

# Database (Render provides this automatically, but you can override)
DATABASE_URL=postgresql://... (Render auto-provides this)

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=True
# OR specify your Vercel domain:
# CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app

# WhatsApp/Twilio Settings (if using)
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=+14155238886
ADMIN_PHONE_NUMBER=+254769582779
ADMIN_DASHBOARD_URL=https://your-frontend.vercel.app/admin-dashboard/
```

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Render will automatically build and deploy your application
3. Wait for deployment to complete (usually 2-5 minutes)
4. Your backend will be available at: `https://your-app-name.onrender.com`

### Step 5: Run Migrations
After first deployment, run migrations:
1. Go to **Shell** tab in Render dashboard
2. Run: `python manage.py migrate`
3. (Optional) Create superuser: `python manage.py createsuperuser`

---

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend
The frontend files are already configured to use environment variables for the API URL.

### Step 2: Create Vercel Project
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your Git repository
4. Configure the project:
   - **Framework Preset**: Other
   - **Root Directory**: `./frontend` (or leave as root if vercel.json handles routing)
   - **Build Command**: Leave empty (static files)
   - **Output Directory**: Leave empty

### Step 3: Set Environment Variables in Vercel
Go to **Settings** → **Environment Variables** and add:

```bash
# API Base URL (your Render backend URL)
NEXT_PUBLIC_API_URL=https://your-app-name.onrender.com
```

**Note**: For static HTML files, we use a different approach. You'll need to:
1. Set the API URL in Vercel environment variables
2. Or update the HTML files to include a script that sets `window.API_URL` before loading config.js

### Step 4: Update Frontend Files for Vercel
Since Vercel doesn't automatically inject env vars into static HTML, we need to update the config.js approach.

**Option A: Use Vercel's Build-time Injection**
Create a `vercel-build.sh` script that replaces placeholders:

```bash
#!/bin/bash
# Replace API_URL placeholder in HTML files
find frontend -name "*.html" -exec sed -i "s|API_URL_PLACEHOLDER|${NEXT_PUBLIC_API_URL}|g" {} \;
```

**Option B: Use HTML Data Attributes (Recommended)**
Update your HTML files to include:
```html
<html data-api-url="https://your-backend.onrender.com">
```

Then update `config.js` to read from this attribute (already implemented).

### Step 5: Deploy
1. Click **"Deploy"**
2. Vercel will build and deploy your frontend
3. Your frontend will be available at: `https://your-project.vercel.app`

---

## Environment Variables Summary

### Backend (Render)
| Variable | Description | Example |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | `your-secret-key` |
| `DJANGO_DEBUG` | Debug mode | `False` |
| `DJANGO_ALLOWED_HOSTS` | Allowed hosts | `your-app.onrender.com` |
| `DATABASE_URL` | PostgreSQL URL | Auto-provided by Render |
| `CORS_ALLOW_ALL_ORIGINS` | Allow all CORS origins | `True` or `False` |
| `CORS_ALLOWED_ORIGINS` | Specific CORS origins | `https://your-frontend.vercel.app` |

### Frontend (Vercel)
| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-backend.onrender.com` |

---

## Post-Deployment Configuration

### 1. Update Frontend API URL
After deploying the backend, update your frontend's API URL:

**Method 1: Update HTML files directly**
Add this to each HTML file's `<html>` tag:
```html
<html lang="en" data-api-url="https://your-backend.onrender.com">
```

**Method 2: Use Vercel Environment Variables**
Create a build script that injects the API URL.

### 2. Test the Connection
1. Open your frontend URL
2. Open browser DevTools → Network tab
3. Try logging in or making an API call
4. Verify requests are going to your Render backend URL

### 3. Update Admin Dashboard URL
Update the `ADMIN_DASHBOARD_URL` environment variable in Render to point to your Vercel frontend.

---

## Troubleshooting

### Backend Issues

**Issue: Database migrations fail**
- Solution: Run migrations manually in Render Shell: `python manage.py migrate`

**Issue: Static files not loading**
- Solution: Ensure `collectstatic` runs in Procfile: `python manage.py collectstatic --noinput`

**Issue: CORS errors**
- Solution: Check `CORS_ALLOW_ALL_ORIGINS` or `CORS_ALLOWED_ORIGINS` settings
- Ensure your frontend URL is in the allowed origins list

### Frontend Issues

**Issue: API calls fail with CORS error**
- Solution: Check backend CORS settings allow your Vercel domain

**Issue: API URL not updating**
- Solution: Clear browser cache, or update HTML files with data-api-url attribute

**Issue: 404 errors on routes**
- Solution: Check `vercel.json` routing configuration

### General Issues

**Issue: Environment variables not working**
- Solution: 
  - Restart the service after adding env vars
  - Check variable names match exactly (case-sensitive)
  - Verify no extra spaces in values

**Issue: Build fails**
- Solution:
  - Check build logs in Render/Vercel dashboard
  - Verify all dependencies are in requirements.txt
  - Check for syntax errors in code

---

## Quick Reference

### Backend URLs
- Health Check: `https://your-backend.onrender.com/`
- API Base: `https://your-backend.onrender.com/api/`
- Admin Panel: `https://your-backend.onrender.com/admin/`

### Frontend URLs
- Home: `https://your-frontend.vercel.app/`
- Login: `https://your-frontend.vercel.app/login/`
- Register: `https://your-frontend.vercel.app/register/`
- Admin Dashboard: `https://your-frontend.vercel.app/admin-dashboard/`

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update API URLs in frontend
4. ✅ Test all functionality
5. ✅ Set up custom domains (optional)
6. ✅ Configure SSL certificates (automatic on both platforms)
7. ✅ Set up monitoring and alerts

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Render/Vercel deployment logs
3. Check Django/Vercel documentation
4. Contact your development team

---

**Last Updated**: 2024
**Version**: 1.0

