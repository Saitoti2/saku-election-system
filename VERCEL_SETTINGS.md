# ⚠️ IMPORTANT: Vercel Project Settings

## The Problem
Vercel is detecting `requirements.txt` and trying to install Python dependencies, which we don't need for the frontend.

## Solution: Change Root Directory in Vercel

### Step 1: Go to Vercel Project Settings
1. Open your Vercel project dashboard
2. Go to **Settings** → **General**
3. Scroll to **Root Directory**

### Step 2: Set Root Directory
Change **Root Directory** from `.` (root) to:
```
frontend
```

### Step 3: Update Build Settings
In the same settings page:
- **Framework Preset**: Other
- **Build Command**: `cd .. && node inject-api-url.js`
- **Output Directory**: (leave empty)

### Step 4: Update vercel.json Location
Since root is now `frontend`, we need to move `vercel.json` OR update the build command.

**Option A: Move vercel.json to frontend/**
```bash
mv vercel.json frontend/
```

**Option B: Keep vercel.json in root and update build command**
The build command above should work.

## Alternative: Use .vercelignore More Effectively

If you can't change root directory, we can:
1. Rename `requirements.txt` to `requirements.txt.backup` during build
2. Or use a build script that handles this

## Recommended Approach
**Set Root Directory to `frontend`** - This is the cleanest solution!

