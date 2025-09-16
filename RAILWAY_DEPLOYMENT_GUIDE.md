# 🚂 Railway Deployment Guide for SAKU Election System

## 📋 Prerequisites
- GitHub repository with your code
- Railway account (free tier available)
- Railway CLI (optional but recommended)

## 🚀 Step-by-Step Deployment

### 1. Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub account

### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository: `saku-election-system`
4. Select the main branch

### 3. Add PostgreSQL Database
1. In your Railway project dashboard
2. Click "New" → "Database" → "PostgreSQL"
3. Railway will automatically create a free PostgreSQL database
4. Note the database connection details

### 4. Configure Environment Variables
In Railway project settings, add these environment variables:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app-name.railway.app

# Database (Railway will provide this automatically)
DATABASE_URL=postgresql://username:password@host:port/database

# WhatsApp Integration (Optional)
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=+14155238886
ADMIN_PHONE_NUMBER=+254769582779

# Admin Dashboard URL
ADMIN_DASHBOARD_URL=https://your-app-name.railway.app/admin-dashboard/
```

### 5. Deploy
1. Railway will automatically detect the Django project
2. It will run the build process using the `start.sh` script
3. The app will be deployed to a Railway subdomain

### 6. Run Database Migrations
After deployment, run migrations:
1. Go to Railway project dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click on the latest deployment
5. Go to "Logs" tab
6. Run: `python manage.py migrate`

### 7. Create Superuser (Optional)
To access Django admin:
```bash
python manage.py createsuperuser
```

## 🔧 Railway Configuration Files

### railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "./start.sh",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### start.sh
```bash
#!/bin/bash
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

## 🌐 Access Your Application

After deployment, your app will be available at:
- **Main App**: `https://your-app-name.railway.app`
- **Admin Dashboard**: `https://your-app-name.railway.app/admin-dashboard/`
- **Django Admin**: `https://your-app-name.railway.app/admin/`

## 📊 Railway Free Tier Limits

- **$5 credit per month** (usually enough for small apps)
- **512MB RAM**
- **1GB storage**
- **PostgreSQL database included**
- **Custom domains supported**

## 🔍 Troubleshooting

### Common Issues:

1. **Build Fails**
   - Check Railway logs for errors
   - Ensure all dependencies are in requirements.txt
   - Verify start.sh is executable

2. **Database Connection Issues**
   - Check DATABASE_URL environment variable
   - Ensure PostgreSQL service is running
   - Run migrations manually if needed

3. **Static Files Not Loading**
   - Check STATIC_ROOT setting
   - Ensure collectstatic runs during deployment
   - Verify WhiteNoise configuration

4. **Environment Variables Not Working**
   - Check Railway project settings
   - Ensure variable names match exactly
   - Redeploy after adding new variables

## 🎯 Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Static files collected
- [ ] DEBUG=False in production
- [ ] ALLOWED_HOSTS configured
- [ ] SSL certificate active (automatic with Railway)
- [ ] Health check endpoint working
- [ ] Admin user created
- [ ] WhatsApp integration tested (if using)

## 🔄 Updates and Maintenance

### Updating Your App:
1. Push changes to GitHub
2. Railway automatically redeploys
3. Check logs for any issues

### Database Backups:
- Railway provides automatic backups
- Download backups from project dashboard
- Restore using Railway CLI or dashboard

## 📞 Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- Railway Status: [status.railway.app](https://status.railway.app)

---

**🎉 Your SAKU Election System is now ready for production deployment on Railway!**
