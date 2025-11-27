# Vercel Frontend Deployment - Step by Step

## Prerequisites
✅ Backend deployed on Render (you mentioned it's done!)
✅ Git repository with all changes committed

## Step 1: Get Your Backend URL
1. Go to your Render dashboard
2. Find your backend service
3. Copy the URL (e.g., `https://saku-backend.onrender.com`)
4. **Save this URL** - you'll need it in Step 4

## Step 2: Go to Vercel
1. Open [https://vercel.com](https://vercel.com)
2. Sign in (or create an account if needed)
3. Click **"Add New..."** → **"Project"**

## Step 3: Import Your Repository
1. Connect your GitHub/GitLab/Bitbucket account if not already connected
2. Find and select your **"SAKU Election System - Render"** repository
3. Click **"Import"**

## Step 4: Configure Project Settings

### Basic Configuration:
- **Project Name**: `saku-election-frontend` (or your preferred name)
- **Framework Preset**: Select **"Other"** (since we're using static HTML)
- **Root Directory**: Leave as **"."** (root) - our vercel.json handles routing
- **Build Command**: `node inject-api-url.js`
- **Output Directory**: Leave empty (we're using static files)

### Environment Variables:
Click **"Environment Variables"** and add:

**Variable Name**: `NEXT_PUBLIC_API_URL`  
**Value**: `https://your-backend-url.onrender.com`  
*(Replace with your actual Render backend URL)*

**Important**: Make sure to:
- ✅ Check "Production"
- ✅ Check "Preview" 
- ✅ Check "Development"

## Step 5: Deploy
1. Click **"Deploy"** button
2. Wait for deployment (usually 1-2 minutes)
3. Vercel will show you the deployment URL (e.g., `https://saku-election-frontend.vercel.app`)

## Step 6: Verify Deployment

### Test the Frontend:
1. Visit your Vercel URL: `https://your-project.vercel.app`
2. You should see the SAKU homepage

### Test API Connection:
1. Open browser DevTools (F12)
2. Go to **Network** tab
3. Try to login or register
4. Check if API calls are going to your Render backend URL
5. Verify there are no CORS errors

## Step 7: Update Backend CORS (if needed)

If you get CORS errors:
1. Go to Render dashboard
2. Find your backend service
3. Go to **Environment** tab
4. Add/Update:
   ```
   CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
   ```
   (Replace with your actual Vercel URL)
5. Redeploy the backend

## Troubleshooting

### Issue: Build fails
- **Solution**: Check that `inject-api-url.js` is in the root directory
- Verify Node.js is available in Vercel (it should be by default)

### Issue: API calls fail
- **Solution**: 
  1. Verify `NEXT_PUBLIC_API_URL` environment variable is set correctly
  2. Check browser console for errors
  3. Verify backend URL is accessible

### Issue: 404 errors on routes
- **Solution**: Check that `vercel.json` is in the root directory

### Issue: API URL not updating
- **Solution**: 
  1. Check environment variable is set
  2. Redeploy after setting environment variable
  3. Clear browser cache

## Next Steps After Deployment

1. ✅ Test all pages:
   - Homepage: `/`
   - Login: `/login/`
   - Register: `/register/`
   - Admin Dashboard: `/admin-dashboard/`
   - Portal: `/portal/`

2. ✅ Test functionality:
   - User registration
   - User login
   - API calls

3. ✅ Share the URL with students!

## Quick Reference

- **Frontend URL**: `https://your-project.vercel.app`
- **Backend URL**: `https://your-backend.onrender.com`
- **Environment Variable**: `NEXT_PUBLIC_API_URL`

---

**Need Help?** Check the main `DEPLOYMENT.md` file for more details.

