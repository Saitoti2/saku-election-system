# Fix: Render Start Command Error

## Problem
Render is trying to run `gunicorn app:app` but this is a Django project. The error shows:
```
ModuleNotFoundError: No module named 'app'
```

## Solution

You have TWO issues to fix:
1. The **Start Command** is wrong
2. The **Root Directory** setting needs to match your actual file structure

### IMPORTANT: Check Your File Structure First

Your Django project files (`manage.py` and `core/`) are at the **root** of your repository, not in `saku-strategy/backend/`.

### Option 1: Use Root Directory (Recommended - Easiest Fix)

1. **Go to your Render Dashboard**
   - Navigate to your web service (the one that's failing)

2. **Go to Settings**
   - Click on your service
   - Click the "Settings" tab (in the left sidebar)

3. **Update Root Directory**
   - Find "Root Directory" field
   - **Leave it EMPTY** or set it to `.` (dot)
   - This tells Render to use the repository root

4. **Update the Start Command**
   - Scroll down to find "Start Command"
   - Replace whatever is there with:
   ```bash
   gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

5. **Update Build Command**
   - Build Command should be:
   ```bash
   pip install -r saku-strategy/backend/requirements.txt && python manage.py collectstatic --noinput
   ```
   (Note: requirements.txt is in `saku-strategy/backend/` but manage.py is at root)

### Option 2: Keep saku-strategy/backend as Root (Alternative)

If you want to use `saku-strategy/backend` as root directory, you need to:
1. Copy `manage.py` from root to `saku-strategy/backend/`
2. Copy `core/` directory from root to `saku-strategy/backend/`
3. Copy `elections/` directory to `saku-strategy/backend/` (if not already there)

But **Option 1 is easier** - just use the root directory!

5. **Verify Build Command**
   - Build Command should be:
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```

6. **Save and Redeploy**
   - Click "Save Changes"
   - Render will automatically trigger a new deployment

---

## Complete Render Configuration Checklist

### Basic Settings:
- **Name**: `saku-backend` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your default branch)
- **Root Directory**: `saku-strategy/backend` ✅
- **Environment**: `Python 3`

### Commands:
- **Build Command**:
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
  
- **Start Command**:
  ```bash
  gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
  ```
  ⚠️ **This is the most important fix!**

### Environment Variables:
Make sure you have these set (see RENDER_ENV_VARIABLES.md):
- `DJANGO_SECRET_KEY` ✅
- `DJANGO_DEBUG=False` ✅
- `DJANGO_ALLOWED_HOSTS=your-service-name.onrender.com` ✅
- `DATABASE_URL` (auto-provided if you linked a PostgreSQL database) ✅

---

## Why This Works

- `core` is your Django project name (located in `saku-strategy/backend/core/`)
- `wsgi` is the WSGI module (located at `saku-strategy/backend/core/wsgi.py`)
- `application` is the WSGI application object

So `core.wsgi:application` tells gunicorn:
- Import the `core` package
- Use the `wsgi` module
- Find the `application` object in that module

---

## After Fixing

1. Render will automatically redeploy
2. Wait 5-10 minutes for the build to complete
3. Check the logs - you should see:
   ```
   ==> Running 'gunicorn core.wsgi:application --bind 0.0.0.0:$PORT...'
   ```
4. If successful, you'll see Django starting up
5. Then you'll need to run migrations (see next steps)

---

## Next Steps After Successful Deployment

1. **Run Migrations**:
   - Go to your service → "Shell" tab
   - Run: `python manage.py migrate`

2. **Create Superuser** (optional):
   - In the shell: `python manage.py createsuperuser`

3. **Test Your Backend**:
   - Visit: `https://your-service-name.onrender.com/api/`
   - You should see a JSON response with "status": "healthy"

---

## Quick Reference

| Setting | Value |
|---------|-------|
| **Root Directory** | `saku-strategy/backend` |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput` |
| **Start Command** | `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120` |

---

## Still Having Issues?

If the error persists after fixing the start command:

1. **Check Root Directory**: Must be exactly `saku-strategy/backend`
2. **Check Build Logs**: Make sure dependencies installed correctly
3. **Check that `core/wsgi.py` exists**: Should be at `saku-strategy/backend/core/wsgi.py`
4. **Verify Python Version**: Render should auto-detect, but you can set `PYTHON_VERSION=3.11.0` in environment variables

