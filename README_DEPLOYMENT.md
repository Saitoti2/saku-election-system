# Quick Deployment Guide

## 🚀 Backend on Render

1. **Connect Repository**: Go to [Render Dashboard](https://dashboard.render.com/) → New Web Service
2. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`
3. **Set Environment Variables**:
   ```
   DJANGO_SECRET_KEY=<generate-a-random-secret-key>
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-app-name.onrender.com
   CORS_ALLOW_ALL_ORIGINS=True
   ```
4. **Deploy** and note your backend URL (e.g., `https://saku-backend.onrender.com`)

## 🎨 Frontend on Vercel

1. **Connect Repository**: Go to [Vercel Dashboard](https://vercel.com/dashboard) → Add New Project
2. **Set Environment Variable**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   ```
   (Use the URL from step 4 above)
3. **Configure**:
   - Framework: Other
   - Root Directory: `frontend` (or leave as root)
   - Build Command: `cd frontend && node ../inject-api-url.js || true`
4. **Deploy**

## ✅ After Deployment

1. Update all HTML files to include: `<html data-api-url="https://your-backend.onrender.com">`
   OR
2. The build script will automatically inject the API URL from `NEXT_PUBLIC_API_URL`

## 🔗 Testing

- Backend: `https://your-backend.onrender.com/` (should show health check)
- Frontend: `https://your-frontend.vercel.app/`
- Test login/registration to verify API connection

## 📚 Full Documentation

See `DEPLOYMENT.md` for detailed instructions and troubleshooting.

