# Environment Variables for Render Deployment

## Required Environment Variables

Add these environment variables in the Render.com dashboard when creating/editing your web service:

### 1. DJANGO_SECRET_KEY (REQUIRED)
**Key:** `DJANGO_SECRET_KEY`  
**Value:** Generate a secure secret key using:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Or use this Python command in your terminal to generate one.

**Example value:** `django-insecure-abc123xyz456...` (use a generated one, not this example)

---

### 2. DJANGO_DEBUG (REQUIRED)
**Key:** `DJANGO_DEBUG`  
**Value:** `False`

**Important:** Always set this to `False` in production for security!

---

### 3. DJANGO_ALLOWED_HOSTS (REQUIRED)
**Key:** `DJANGO_ALLOWED_HOSTS`  
**Value:** Your Render service URL (e.g., `saku-backend.onrender.com`)

**Example:** `saku-backend.onrender.com,your-custom-domain.com`

**Note:** After deployment, Render will give you a URL like `https://your-service-name.onrender.com`. Use just the domain part (without `https://`).

---

### 4. DATABASE_URL (OPTIONAL - Auto-provided)
**Key:** `DATABASE_URL`  
**Value:** Auto-provided by Render if you create a PostgreSQL database first

**Steps:**
1. First, create a PostgreSQL database in Render (New + → PostgreSQL)
2. Render automatically creates the `DATABASE_URL` environment variable
3. You can manually add it to your web service, or Render will link it automatically

**If not using a database yet:** You can leave this out initially, but the app requires a database to function properly.

---

## Optional Environment Variables

### 5. VERCEL_FRONTEND_URL (RECOMMENDED)
**Key:** `VERCEL_FRONTEND_URL`  
**Value:** Your Vercel frontend URL (e.g., `https://your-project.vercel.app`)

Add this after you deploy your frontend to Vercel. This allows CORS to work properly.

---

### 6. WhatsApp Configuration (OPTIONAL)
Only add these if you're using WhatsApp notifications:

**Key:** `WHATSAPP_API_URL`  
**Value:** `https://graph.facebook.com/v18.0`

**Key:** `WHATSAPP_API_TOKEN`  
**Value:** Your Meta WhatsApp API token

**Key:** `WHATSAPP_PHONE_NUMBER_ID`  
**Value:** Your WhatsApp phone number ID

**Key:** `ADMIN_PHONE_NUMBER`  
**Value:** `+254769582779` (your admin WhatsApp number)

---

### 7. Twilio Configuration (OPTIONAL)
Only add these if you're using Twilio as a fallback:

**Key:** `TWILIO_ACCOUNT_SID`  
**Value:** Your Twilio Account SID

**Key:** `TWILIO_AUTH_TOKEN`  
**Value:** Your Twilio Auth Token

**Key:** `TWILIO_WHATSAPP_NUMBER`  
**Value:** `+14155238886` (Twilio WhatsApp number)

---

## Quick Setup Guide

### Step 1: Generate Secret Key
Run this command locally to generate your secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output.

### Step 2: Add Environment Variables in Render
1. In the Render dashboard, go to your web service (or create a new one)
2. Click on "Environment" tab (or "Add Environment Variable" section)
3. Click "+ Add Environment Variable" for each variable
4. Add these three REQUIRED ones first:

```
Key: DJANGO_SECRET_KEY
Value: [paste your generated secret key]

Key: DJANGO_DEBUG
Value: False

Key: DJANGO_ALLOWED_HOSTS
Value: your-service-name.onrender.com
```

### Step 3: Create Database (if not done)
1. Go to Render dashboard → New + → PostgreSQL
2. Create a database named `saku-db`
3. Render will automatically provide the `DATABASE_URL` environment variable

### Step 4: Deploy!
Click "Deploy Web Service" or "Save Changes"

---

## Environment Variables Summary Table

| Variable | Required? | Example Value | Notes |
|----------|-----------|---------------|-------|
| `DJANGO_SECRET_KEY` | ✅ YES | `django-insecure-abc...` | Generate using Python command |
| `DJANGO_DEBUG` | ✅ YES | `False` | Must be `False` in production |
| `DJANGO_ALLOWED_HOSTS` | ✅ YES | `saku-backend.onrender.com` | Your Render domain |
| `DATABASE_URL` | ✅ YES* | Auto-provided | Created when you add PostgreSQL |
| `VERCEL_FRONTEND_URL` | ⚠️ Recommended | `https://your-app.vercel.app` | Add after frontend deployment |
| `WHATSAPP_API_TOKEN` | ❌ Optional | Your token | Only if using WhatsApp |
| `TWILIO_ACCOUNT_SID` | ❌ Optional | Your SID | Only if using Twilio |

*Required for the app to function, but Render provides it automatically when you create a database.

---

## Troubleshooting

**"Invalid SECRET_KEY" error:**
- Make sure you generated a proper secret key
- Check for typos when copying

**"DisallowedHost" error:**
- Make sure `DJANGO_ALLOWED_HOSTS` matches your Render URL exactly
- No `https://` prefix, just the domain

**Database connection errors:**
- Verify `DATABASE_URL` is set (check Environment tab)
- Make sure PostgreSQL database service is running
- Database might take a few minutes to provision

**CORS errors:**
- Add `VERCEL_FRONTEND_URL` environment variable
- Ensure your frontend URL matches exactly

---

## After Deployment

Once deployed, you can update environment variables at any time:
1. Go to your Render service → Environment tab
2. Click "Add Environment Variable" or edit existing ones
3. Render will automatically redeploy when you save changes

