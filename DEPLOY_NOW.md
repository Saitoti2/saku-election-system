# 🚀 Deploy Frontend to Vercel - Ready to Go!

## ✅ Your Backend URL
**Backend**: `https://saku-elections.onrender.com`

---

## 📋 Step-by-Step Vercel Deployment

### Step 1: Go to Vercel
👉 Open: [https://vercel.com/dashboard](https://vercel.com/dashboard)
- Sign in or create account

### Step 2: Create New Project
1. Click **"Add New..."** button (top right)
2. Select **"Project"**

### Step 3: Import Repository
1. Connect your Git provider (GitHub/GitLab/Bitbucket) if needed
2. Find and select: **"SAKU Election System - Render"**
3. Click **"Import"**

### Step 4: Configure Project

**Project Settings:**
- **Project Name**: `saku-election-frontend` (or your choice)
- **Framework Preset**: **Other** ⚠️ (Important: Select "Other", not a framework)
- **Root Directory**: `.` (leave as root - don't change)
- **Build Command**: `node inject-api-url.js` ⚠️ (Must be exactly this)
- **Output Directory**: (leave empty)

### Step 5: Add Environment Variable ⚠️ CRITICAL

1. **Before clicking Deploy**, click **"Environment Variables"** section
2. Click **"Add"** button
3. Enter:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://saku-elections.onrender.com`
4. **Check all three boxes**:
   - ✅ Production
   - ✅ Preview
   - ✅ Development
5. Click **"Add"** to save

### Step 6: Deploy!
1. Click the big **"Deploy"** button
2. Wait 1-2 minutes for build to complete
3. ✅ Your frontend will be live!

---

## 🔧 Fix Backend ALLOWED_HOSTS (If Needed)

If you see 400 errors from backend, update Render environment:

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Select your backend service: `saku-elections`
3. Go to **"Environment"** tab
4. Add/Update:
   ```
   DJANGO_ALLOWED_HOSTS=saku-elections.onrender.com,localhost,127.0.0.1
   ```
5. Save and redeploy

---

## ✅ After Deployment - Test

1. **Visit your Vercel URL** (shown after deployment)
2. **Open Browser DevTools** (F12)
3. **Go to Network tab**
4. **Try to login or register**
5. **Check if API calls are going to**: `https://saku-elections.onrender.com`

### Expected Results:
- ✅ Frontend loads correctly
- ✅ API calls go to your Render backend
- ✅ No CORS errors in console
- ✅ Login/Registration works

---

## 🆘 Troubleshooting

### Build Fails
- Check that `inject-api-url.js` is in root directory
- Verify Node.js is available (should be automatic)

### API Calls Fail
- Verify `NEXT_PUBLIC_API_URL` environment variable is set
- Check backend is accessible: `https://saku-elections.onrender.com`
- Check browser console for errors

### CORS Errors
- Update Render backend: `CORS_ALLOW_ALL_ORIGINS=True`
- Or add: `CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app`

### 404 on Routes
- Verify `vercel.json` is in root directory
- Check routing configuration

---

## 📝 Quick Reference

| Item | Value |
|------|-------|
| Backend URL | `https://saku-elections.onrender.com` |
| Environment Variable | `NEXT_PUBLIC_API_URL` |
| Environment Value | `https://saku-elections.onrender.com` |
| Build Command | `node inject-api-url.js` |

---

**Ready? Let's deploy! 🚀**

Follow steps 1-6 above, and you'll have your frontend live in minutes!

