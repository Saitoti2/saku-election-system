# Frontend Deployment Guide - Step by Step

This guide will walk you through deploying your SAKU Election System frontend to Vercel.

## Prerequisites Checklist ✅

- [x] Backend deployed on Render: `https://saku-election-system-2.onrender.com`
- [x] Frontend code is ready in the `frontend/` directory
- [x] GitHub repository is up to date
- [x] Vercel account (sign up at [vercel.com](https://vercel.com) if needed)

---

## Step 1: Update Backend URL in Frontend Config

✅ **DONE**: I've already updated `frontend/api-config.js` and `frontend/config.js` with your Render backend URL:
- Backend URL: `https://saku-election-system-2.onrender.com`

---

## Step 2: Commit and Push the Updated Config

The API configuration has been updated. Let's commit and push it:

```bash
git add frontend/api-config.js frontend/config.js
git commit -m "Update frontend API config with Render backend URL"
git push origin main
```

---

## Step 3: Go to Vercel Dashboard

1. Open your browser and go to: **https://vercel.com**
2. Click **"Login"** or **"Sign Up"** if you don't have an account
3. Sign in with GitHub (recommended) to connect your repository easily

---

## Step 4: Import Your Project

1. In Vercel dashboard, click **"Add New..."** button (top right)
2. Select **"Project"** from the dropdown
3. Click **"Import Git Repository"**
4. Find and select your repository: `Saitoti2/saku-election-system`
5. Click **"Import"**

---

## Step 5: Configure Project Settings

You'll see the configuration page. Fill in these settings:

### Project Name
- **Name**: `saku-election-frontend` (or any name you prefer)

### Framework Preset
- **Framework Preset**: Select **"Other"** or **"Static"**

### Root Directory
- **Root Directory**: Click "Edit" and set to: **`frontend`**

### Build and Output Settings
- **Build Command**: Leave **EMPTY** (we're serving static files)
- **Output Directory**: Set to **`.`** (current directory)
- **Install Command**: Leave **EMPTY**

---

## Step 6: Add Environment Variables

1. Scroll down to **"Environment Variables"** section
2. Click **"Add"** to add a new environment variable

### Add This Variable:
- **Key**: `API_BASE_URL`
- **Value**: `https://saku-election-system-2.onrender.com`
- **Environment**: Select **Production**, **Preview**, and **Development** (or just **Production**)

3. Click **"Add"** to save

---

## Step 7: Deploy!

1. Scroll down and review all settings
2. Click the big **"Deploy"** button
3. Wait for deployment to complete (usually 1-2 minutes)

---

## Step 8: Monitor Deployment

You'll see a build log showing:
- ✅ Installing dependencies
- ✅ Building project
- ✅ Deploying to production

Wait until you see:
- ✅ **"Ready"** status
- ✅ Your deployment URL (e.g., `https://saku-election-frontend.vercel.app`)

---

## Step 9: Update Backend CORS Settings

After deployment, you need to tell your Render backend to allow requests from your Vercel frontend:

1. Go to your **Render Dashboard**: https://dashboard.render.com
2. Select your backend service: **`saku-election-system-2`**
3. Go to **"Environment"** tab
4. Click **"Add Environment Variable"**
5. Add:
   - **Key**: `VERCEL_FRONTEND_URL`
   - **Value**: `https://your-frontend-name.vercel.app` (replace with your actual Vercel URL)
6. Click **"Save Changes"**
7. Render will automatically redeploy (wait 5-10 minutes)

---

## Step 10: Test Your Deployment

1. Visit your Vercel frontend URL
2. Try accessing: `https://your-frontend-name.vercel.app`
3. Open browser console (F12) to check for errors
4. Try logging in or creating an account
5. Check if API calls are working

---

## Troubleshooting

### Frontend shows but can't connect to backend

**Solution**: Check that:
- `API_BASE_URL` environment variable is set in Vercel
- Backend CORS settings include your Vercel URL
- Backend is running and accessible

### CORS errors in browser console

**Solution**: 
1. Add `VERCEL_FRONTEND_URL` to Render backend environment variables
2. Wait for backend to redeploy
3. Clear browser cache and reload

### 404 errors on routes

**Solution**: Check that `vercel.json` is in the `frontend/` directory with proper routing rules.

---

## Quick Reference

| Setting | Value |
|---------|-------|
| **Root Directory** | `frontend` |
| **Build Command** | (empty) |
| **Output Directory** | `.` |
| **Environment Variable** | `API_BASE_URL=https://saku-election-system-2.onrender.com` |

---

## Next Steps After Deployment

1. ✅ Test all frontend pages
2. ✅ Test login/registration
3. ✅ Test API connectivity
4. ✅ Share the Vercel URL with your team
5. ✅ (Optional) Set up custom domain

---

## Need Help?

- Check Vercel deployment logs
- Check browser console for errors
- Verify environment variables are set correctly
- Ensure backend is running and accessible

