# Railway Deployment Configuration

## Environment Variables to Set in Railway Dashboard

```
SECRET_KEY=your-production-secret-key-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=*.railway.app
ADMIN_PHONE_NUMBER=+254769582779
```

## Railway-Specific Configuration

The deployment includes:
- ✅ Health check endpoint at `/` 
- ✅ Proper Gunicorn configuration with workers and timeouts
- ✅ Static files collection during deployment
- ✅ Railway-specific Django settings
- ✅ Automatic database migration on startup

## Optional Environment Variables

```
# WhatsApp Configuration
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id

# Twilio Configuration
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

## Railway Setup Steps

1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub account
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add the environment variables above
6. Deploy!

## Troubleshooting

If deployment fails:
- Check that all dependencies are in requirements.txt
- Ensure Procfile is correct
- Verify environment variables are set
- Check Railway logs for specific errors
