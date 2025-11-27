# Deployment Guide: SAKU Election System

This guide will help you deploy the SAKU Election System to Render (backend) and Vercel (frontend).

## Prerequisites

- A GitHub account (or GitLab/Bitbucket)
- A Render account (free tier available)
- A Vercel account (free tier available)
- Your code pushed to a Git repository

## Part 1: Backend Deployment on Render

### Step 1: Prepare Your Repository

1. Make sure all your code is committed and pushed to your Git repository
2. Ensure `requirements.txt` is up to date in `saku-strategy/backend/`
3. The `render.yaml` file is already configured in `saku-strategy/backend/`

### Step 2: Deploy on Render

1. **Sign up/Login to Render**: Go to [render.com](https://render.com) and sign up or log in

2. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Select the repository containing this project

3. **Configure the Service**:
   - **Name**: `saku-backend` (or your preferred name)
   - **Region**: Choose closest to your users (e.g., Oregon)
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `saku-strategy/backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput
     ```
   - **Start Command**:
     ```bash
     gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
     ```

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable" and add:
   
   ```
   DJANGO_SECRET_KEY=your-secret-key-here (generate a strong random key)
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=saku-backend.onrender.com,your-custom-domain.com
   DATABASE_URL=(Render will auto-provide this if you create a database)
   VERCEL_FRONTEND_URL=https://your-frontend.vercel.app
   ```
   
   **Important**: Generate a secure secret key:
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

5. **Create a PostgreSQL Database**:
   - Click "New +" → "PostgreSQL"
   - Name it `saku-db`
   - Render will automatically provide the `DATABASE_URL` environment variable
   - Copy the database URL and add it to your web service environment variables

6. **Deploy**:
   - Click "Create Web Service"
   - Render will start building and deploying your application
   - Wait for the build to complete (usually 5-10 minutes)

7. **Run Migrations**:
   Once deployed, you need to run migrations. You can do this via Render's shell:
   - Go to your service → "Shell"
   - Run: `python manage.py migrate`
   - Or create a superuser: `python manage.py createsuperuser`

8. **Note Your Backend URL**:
   Your backend will be available at: `https://saku-backend.onrender.com`
   (or your custom domain if configured)

## Part 2: Frontend Deployment on Vercel

### Step 1: Prepare Frontend

The frontend files are already configured with `api-config.js` that will automatically detect the backend URL.

### Step 2: Deploy on Vercel

1. **Sign up/Login to Vercel**: Go to [vercel.com](https://vercel.com) and sign up or log in

2. **Import Your Project**:
   - Click "Add New..." → "Project"
   - Import your Git repository
   - Select the repository

3. **Configure the Project**:
   - **Framework Preset**: Other (or leave as default)
   - **Root Directory**: `saku-strategy/frontend`
   - **Build Command**: (leave empty - static files)
   - **Output Directory**: `.` (current directory)
   - **Install Command**: (leave empty)

4. **Add Environment Variables**:
   Click "Environment Variables" and add:
   
   ```
   API_BASE_URL=https://saku-backend.onrender.com
   ```
   
   **Important**: Replace `saku-backend.onrender.com` with your actual Render backend URL

5. **Update api-config.js** (if needed):
   The `api-config.js` file has a fallback URL. Update line 30 in `saku-strategy/frontend/api-config.js`:
   ```javascript
   : 'https://saku-backend.onrender.com'; // Replace with your Render backend URL
   ```

6. **Deploy**:
   - Click "Deploy"
   - Vercel will deploy your frontend (usually 1-2 minutes)
   - Your frontend will be available at: `https://your-project.vercel.app`

## Part 3: Post-Deployment Configuration

### Update Backend CORS Settings

1. Go to your Render dashboard → Your backend service → Environment
2. Add/Update `VERCEL_FRONTEND_URL` with your Vercel frontend URL:
   ```
   VERCEL_FRONTEND_URL=https://your-project.vercel.app
   ```
3. Redeploy the backend service (Render will auto-redeploy when env vars change)

### Update Frontend API Configuration

The frontend will automatically use the correct backend URL based on:
1. Environment variables (if set via Vercel)
2. The fallback URL in `api-config.js`
3. LocalStorage override (for development)

### Test the Deployment

1. Visit your Vercel frontend URL
2. Try logging in or creating an account
3. Check browser console for any CORS or API errors
4. Verify API calls are going to your Render backend

## Part 4: Custom Domain (Optional)

### Backend (Render)

1. Go to Render dashboard → Your service → Settings
2. Click "Custom Domains"
3. Add your domain and follow DNS configuration instructions

### Frontend (Vercel)

1. Go to Vercel dashboard → Your project → Settings → Domains
2. Add your custom domain
3. Configure DNS as instructed by Vercel

## Troubleshooting

### Backend Issues

**Database Connection Errors**:
- Verify `DATABASE_URL` is set correctly in Render environment variables
- Check that the database service is running
- Ensure migrations have been run

**Static Files Not Loading**:
- Verify `collectstatic` ran during build
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Ensure WhiteNoise is installed and configured

**CORS Errors**:
- Verify `VERCEL_FRONTEND_URL` is set in backend environment variables
- Check `ALLOWED_ORIGINS` in settings.py includes your frontend URL
- Ensure `django-cors-headers` is in requirements.txt

### Frontend Issues

**API Calls Failing**:
- Check browser console for errors
- Verify `API_BASE_URL` in Vercel environment variables
- Update the fallback URL in `api-config.js` if needed
- Check CORS settings on backend

**404 Errors on Routes**:
- Verify `vercel.json` is in the frontend root directory
- Check that routes are configured correctly

## Environment Variables Summary

### Backend (Render)
```
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=saku-backend.onrender.com
DATABASE_URL=(auto-provided by Render)
VERCEL_FRONTEND_URL=https://your-frontend.vercel.app
WHATSAPP_API_TOKEN=(if using WhatsApp)
TWILIO_ACCOUNT_SID=(if using Twilio)
ADMIN_PHONE_NUMBER=+254769582779
```

### Frontend (Vercel)
```
API_BASE_URL=https://saku-backend.onrender.com
```

## Security Checklist

- [ ] `DJANGO_DEBUG=False` in production
- [ ] Strong `DJANGO_SECRET_KEY` generated
- [ ] `ALLOWED_HOSTS` set to specific domains (not `*`)
- [ ] CORS configured to allow only your frontend domain
- [ ] Database credentials secured
- [ ] API tokens stored in environment variables (not in code)
- [ ] HTTPS enabled (automatic on Render and Vercel)

## Support

For issues:
1. Check Render logs: Dashboard → Your service → Logs
2. Check Vercel logs: Dashboard → Your project → Deployments → View Function Logs
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly

## Next Steps

After deployment:
1. Create a superuser account for admin access
2. Set up your first election
3. Configure WhatsApp/Twilio if using notifications
4. Test the complete user flow
5. Monitor logs for any errors

