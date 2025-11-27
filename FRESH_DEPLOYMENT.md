# 🚀 Fresh Vercel Deployment Guide

## Step 1: Delete Old Vercel Project (Optional but Recommended)

1. Go to: https://vercel.com/dashboard
2. Find your project: **"saku-election"**
3. Click on it
4. Go to **Settings** → Scroll to bottom
5. Click **"Delete Project"**
6. Confirm deletion

## Step 2: Create New Vercel Project

1. Go to: https://vercel.com/dashboard
2. Click **"Add New..."** → **"Project"**
3. **Import Git Repository:**
   - Find: **"saku-election-system"**
   - Click **"Import"**

## Step 3: Configure New Project

### Basic Settings:
- **Project Name**: `saku-election-frontend` (or your choice)
- **Framework Preset**: **Other** ⚠️ (Important!)
- **Root Directory**: `.` (leave as root - don't change)
- **Build Command**: (leave EMPTY)
- **Output Directory**: (leave EMPTY)
- **Install Command**: (leave EMPTY)

### Environment Variables:
Click **"Environment Variables"** and add:

**Name**: `NEXT_PUBLIC_API_URL`  
**Value**: `https://saku-elections.onrender.com`  
**Environments**: ✅ Production, ✅ Preview, ✅ Development

## Step 4: Deploy

1. Click **"Deploy"** button
2. Wait for deployment (1-2 minutes)
3. ✅ Your frontend will be live!

## Step 5: Update HTML Files with API URL

After deployment, you need to update the HTML files to use your backend URL. The `config.js` file will handle this, but you may need to set the API URL in the HTML files.

**Option A: Update HTML files directly**
Add this to each HTML file's `<html>` tag:
```html
<html lang="en" data-api-url="https://saku-elections.onrender.com">
```

**Option B: Use environment variable**
The `config.js` will read from `NEXT_PUBLIC_API_URL` environment variable.

## What's Different in This Fresh Setup

✅ **Clean vercel.json** - No build commands, just routing
✅ **No install command** - Vercel won't try to install Python
✅ **Simple static file serving** - Just serves frontend files
✅ **Proper routing** - All routes configured correctly

## Expected Result

- ✅ No Python installation attempts
- ✅ No build errors
- ✅ Frontend files served correctly
- ✅ All routes working
- ✅ API calls go to your Render backend

## Troubleshooting

### If deployment fails:
1. Check deployment logs
2. Verify Framework Preset is "Other"
3. Make sure Build Command is empty
4. Verify Root Directory is `.` (root)

### If API calls fail:
1. Check `NEXT_PUBLIC_API_URL` environment variable is set
2. Verify backend URL: `https://saku-elections.onrender.com`
3. Check browser console for CORS errors
4. Update HTML files with `data-api-url` attribute

---

**This fresh deployment should work perfectly!** 🎯

