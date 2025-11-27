# Quick Deployment Checklist

## Backend (Render) - 5 Minutes

1. ✅ Go to [render.com](https://render.com) → New Web Service
2. ✅ Connect your Git repository
3. ✅ Configure:
   - **Root Directory**: `saku-strategy/backend`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
4. ✅ Add Environment Variables:
   ```
   DJANGO_SECRET_KEY=<generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
   DJANGO_DEBUG=False
   DJANGO_ALLOWED_HOSTS=saku-backend.onrender.com
   ```
5. ✅ Create PostgreSQL database → Copy `DATABASE_URL`
6. ✅ Add `DATABASE_URL` to environment variables
7. ✅ Deploy → Wait for build
8. ✅ Run migrations: Render Shell → `python manage.py migrate`
9. ✅ Create superuser: `python manage.py createsuperuser`
10. ✅ Copy your backend URL: `https://saku-backend.onrender.com`

## Frontend (Vercel) - 3 Minutes

1. ✅ Go to [vercel.com](https://vercel.com) → Add New Project
2. ✅ Import your Git repository
3. ✅ Configure:
   - **Root Directory**: `saku-strategy/frontend`
   - **Framework Preset**: Other
4. ✅ Update `api-config.js` line 30 with your Render backend URL:
   ```javascript
   return 'https://saku-backend.onrender.com'; // Your actual Render URL
   ```
5. ✅ Deploy → Done!

## Post-Deployment

1. ✅ Update backend `VERCEL_FRONTEND_URL` env var with your Vercel URL
2. ✅ Test login/registration on frontend
3. ✅ Check browser console for errors

## Important URLs to Update

After deployment, update these in your code:

1. **Frontend** (`saku-strategy/frontend/api-config.js` line 30):
   - Replace `https://saku-backend.onrender.com` with your actual Render URL

2. **Backend** (Render Environment Variables):
   - Add `VERCEL_FRONTEND_URL=https://your-project.vercel.app`

That's it! Your system should be live. 🚀

