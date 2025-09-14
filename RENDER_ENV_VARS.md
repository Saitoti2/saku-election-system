# 🔧 Render.com Environment Variables

## Copy & Paste These Variables into Render Dashboard:

### **Required Variables:**

```
SECRET_KEY=django-insecure-production-key-change-this-12345
DEBUG=False
ALLOWED_HOSTS=*.onrender.com
ADMIN_PHONE_NUMBER=+254769582779
```

### **Optional Variables (if you want WhatsApp notifications):**

```
WHATSAPP_API_URL=https://graph.facebook.com/v18.0
WHATSAPP_API_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_WHATSAPP_NUMBER=+14155238886
```

## 📋 **How to Add Variables in Render:**

1. **Go to your Render service dashboard**
2. **Click "Environment" tab**
3. **Click "Add Environment Variable"**
4. **Copy each variable above** (Key = left side, Value = right side)
5. **Click "Save Changes"**

## 🎯 **Minimum Required Variables:**

For basic deployment, you only need these 4:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | `django-insecure-production-key-change-this-12345` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*.onrender.com` |
| `ADMIN_PHONE_NUMBER` | `+254769582779` |

## 🔒 **Security Note:**

Change the `SECRET_KEY` to something unique for production:
- Generate a random string
- Keep it secret
- Don't share it publicly

## ✅ **Ready to Deploy!**

Once you add these variables, your SAKU Election System will deploy successfully on Render!
