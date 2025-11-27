# Vercel Deployment Configuration

## Your Backend URL
**Backend URL**: `https://saku-elections.onrender.com`

## Environment Variable to Set in Vercel

**Variable Name**: `NEXT_PUBLIC_API_URL`  
**Variable Value**: `https://saku-elections.onrender.com`

Make sure to enable this for:
- ✅ Production
- ✅ Preview  
- ✅ Development

## Quick Deployment Steps

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your repository: **"SAKU Election System - Render"**
4. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `.` (root)
   - **Build Command**: `node inject-api-url.js`
   - **Output Directory**: (leave empty)
5. **Add Environment Variable**:
   - Name: `NEXT_PUBLIC_API_URL`
   - Value: `https://saku-elections.onrender.com`
   - Enable for: Production, Preview, Development
6. Click **"Deploy"**

## After Deployment

Your frontend will be available at: `https://your-project-name.vercel.app`

Test the connection:
- Visit: `https://your-project-name.vercel.app`
- Try logging in
- Check browser console (F12) → Network tab to verify API calls

## Backend CORS Configuration

If you get CORS errors, update your Render backend environment variables:
- Go to Render Dashboard → Your Service → Environment
- Add/Update: `CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app`
- Or keep: `CORS_ALLOW_ALL_ORIGINS=True` (already set)

