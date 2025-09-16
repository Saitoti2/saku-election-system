# 🚀 Render Deployment Guide - SAKU Election System

## 📋 Prerequisites

1. **GitHub Repository** - Push your code to GitHub
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **Domain Name** (Optional) - For custom domain

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Repository

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "SAKU Election System ready for deployment"
   git push origin main
   ```

### Step 2: Create Render Web Service

1. **Go to Render Dashboard**
2. **Click "New +"** → **"Web Service"**
3. **Connect GitHub Repository**
4. **Select your SAKU Election System repository**

### Step 3: Configure Web Service

**Basic Settings:**
- **Name**: `saku-election-system`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `./start.sh`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (recommended)
- **Health Check Path**: `/` (health check endpoint)

### Step 4: Create PostgreSQL Database

1. **Go to Render Dashboard**
2. **Click "New +"** → **"PostgreSQL"**
3. **Configure Database**:
   - **Name**: `saku-election-db`
   - **Database**: `saku_election`
   - **User**: `saku_user`
   - **Region**: Same as web service

### Step 5: Configure Environment Variables

In your Web Service settings, add these environment variables:

**Required Variables:**
```env
DATABASE_URL=postgresql://saku_user:password@host:port/saku_election
SECRET_KEY=your-very-secure-secret-key-here-make-it-long-and-random
DEBUG=False
ALLOWED_HOSTS=saku-election-system.onrender.com
```

**Optional WhatsApp Variables:**
```env
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-whatsapp-business-api-token
WHATSAPP_PHONE_NUMBER_ID=your-whatsapp-phone-number-id
ADMIN_PHONE_NUMBER=+254769582779
```

**Optional Twilio Variables:**
```env
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

### Step 6: Deploy! 🎉

1. **Click "Create Web Service"**
2. **Wait for deployment** (5-10 minutes)
3. **Check build logs** for any errors
4. **Test your application**

## 🔍 Post-Deployment Checklist

### ✅ Verify Deployment

1. **Health Check**: Visit `https://your-app.onrender.com/`
   - Should show: `{"status": "healthy", "message": "SAKU Election System is running"}`

2. **Admin Panel**: Visit `https://your-app.onrender.com/admin/`
   - Login: `admin` / `admin123`

3. **Frontend Pages**: Test all pages:
   - Login: `/login/`
   - Registration: `/register/`
   - Admin Dashboard: `/admin-dashboard/`
   - Student Portal: `/portal/`

4. **API Endpoints**: Test API:
   - `/api/` (should require authentication)
   - `/api/faculties/` (should return empty list initially)

### ✅ Database Verification

1. **Check Admin Panel**:
   - Go to `/admin/`
   - Verify all models are present
   - Check if superuser was created

2. **Test Registration**:
   - Try registering a new user
   - Check if data is saved to database

### ✅ WhatsApp Integration (Optional)

1. **Configure WhatsApp Business API**:
   - Get API token from Meta Business
   - Add phone number ID
   - Test notification sending

2. **Configure Twilio** (Alternative):
   - Set up Twilio WhatsApp sandbox
   - Add credentials to environment variables

## 🛠️ Troubleshooting

### Common Issues

**1. Build Fails**
- Check `requirements.txt` for syntax errors
- Ensure all dependencies are listed
- Check Python version compatibility

**2. Database Connection Error**
- Verify `DATABASE_URL` is correct
- Check if PostgreSQL service is running
- Ensure database credentials are valid

**3. Static Files Not Loading**
- Check if `collectstatic` ran successfully
- Verify `STATIC_ROOT` setting
- Check file permissions

**4. 404 Errors on Frontend Pages**
- Verify URL patterns in `core/urls.py`
- Check if frontend files exist
- Ensure proper file paths

### Debug Mode

To enable debug mode temporarily:
```env
DEBUG=True
ALLOWED_HOSTS=*
```

**⚠️ Never use DEBUG=True in production!**

## 📊 Monitoring

### Render Dashboard
- **Metrics**: CPU, Memory, Response Time
- **Logs**: Application and build logs
- **Health**: Service status monitoring

### Application Logs
- **Access Logs**: Request/response logs
- **Error Logs**: Application errors
- **Database Logs**: Query performance

## 🔄 Updates & Maintenance

### Deploying Updates
1. **Push changes to GitHub**
2. **Render auto-deploys** (if enabled)
3. **Monitor deployment logs**
4. **Test updated features**

### Database Migrations
- **Automatic**: Migrations run during deployment
- **Manual**: Use Render shell for complex migrations

### Backup Strategy
- **Database Backups**: Render provides automatic backups
- **Code Backups**: GitHub repository
- **File Backups**: Consider external storage for media files

## 💰 Cost Optimization

### Free Tier Limits
- **Web Service**: 750 hours/month
- **PostgreSQL**: 1GB storage, 1GB bandwidth
- **Custom Domains**: Not available on free tier

### Upgrade Considerations
- **Starter Plan**: $7/month for always-on service
- **Standard Plan**: $25/month for production use
- **Pro Plan**: $85/month for high-traffic applications

## 🎯 Performance Tips

1. **Enable Caching**: Use Redis for session storage
2. **CDN**: Use Cloudflare for static file delivery
3. **Database Optimization**: Add indexes for frequently queried fields
4. **Image Optimization**: Compress uploaded images
5. **Code Splitting**: Minimize JavaScript bundle size

## 📞 Support

### Render Support
- **Documentation**: [render.com/docs](https://render.com/docs)
- **Community**: [render.com/community](https://render.com/community)
- **Support**: Available on paid plans

### SAKU Election System Support
- **Technical Issues**: Check logs and error messages
- **Feature Requests**: Contact development team
- **Emergency**: Use admin panel for immediate fixes

---

**🎉 Congratulations! Your SAKU Election System is now live on Render!**

**Live URL**: `https://your-app-name.onrender.com`
**Admin Panel**: `https://your-app-name.onrender.com/admin/`
**Login**: `admin` / `admin123`
