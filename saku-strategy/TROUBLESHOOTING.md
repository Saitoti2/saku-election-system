# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. Backend Issues

#### Port 8000 Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
python manage.py runserver 0.0.0.0:8001
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
cd backend
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Database Issues
```bash
# Reset database
cd backend
source .venv/bin/activate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### CORS Issues
- Ensure `django-cors-headers` is installed
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Verify frontend is running on http://localhost:5173

### 2. Frontend Issues

#### Node.js Not Found
```bash
# Install Node.js (macOS with Homebrew)
brew install node

# Or download from https://nodejs.org/
```

#### Port 5173 Already in Use
```bash
# Find process using port 5173
lsof -i :5173

# Kill the process
kill -9 <PID>

# Or use a different port
npm run dev -- --port 5174
```

#### Module Not Found Errors
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### API Connection Issues
- Check if backend is running on http://localhost:8000
- Verify CORS settings in backend
- Check browser console for errors
- Ensure Vite proxy is configured correctly

### 3. Docker Issues

#### Docker Not Running
```bash
# Start Docker Desktop
# Or install Docker
brew install docker
```

#### Container Build Failures
```bash
# Clean Docker cache
docker system prune -a

# Rebuild containers
docker compose down
docker compose up --build --force-recreate
```

### 4. Data Issues

#### No Data Showing
```bash
# Seed sample data
cd backend
source .venv/bin/activate
PYTHONPATH=. python scripts/seed_sample_data.py
```

#### Parsing Errors
- Check if PDFs are in `uploads/` directory
- Verify PDFs are not corrupted
- Check parsing logs in `reports/` directory

### 5. Performance Issues

#### Slow Loading
- Check database size
- Clear browser cache
- Restart servers
- Check system resources

#### Memory Issues
```bash
# Check Python memory usage
ps aux | grep python

# Restart backend
pkill -f "python manage.py runserver"
```

### 6. Security Issues

#### CSRF Token Errors
- Add CSRF token to forms
- Check CSRF settings in Django
- Verify middleware configuration

#### Permission Errors
```bash
# Fix file permissions
chmod +x start.sh
chmod +x scripts/*.sh
```

### 7. Development Issues

#### Tests Failing
```bash
# Run tests with verbose output
cd backend
source .venv/bin/activate
python manage.py test --verbosity=2

# Run specific test
python manage.py test tests.test_api.DelegateAPITest.test_create_delegate
```

#### Import Errors
- Check Python path
- Verify virtual environment is activated
- Check for circular imports

### 8. Production Issues

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Configure static file serving
# Add to settings.py:
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

#### Database Connection Issues
- Check DATABASE_URL
- Verify database credentials
- Check network connectivity

### 9. Logging and Debugging

#### Enable Debug Logging
```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

#### Check Logs
```bash
# Backend logs
tail -f backend/debug.log

# Frontend logs (in browser console)
# Press F12 -> Console tab
```

### 10. Quick Fixes

#### Reset Everything
```bash
# Stop all services
pkill -f "python manage.py runserver"
pkill -f "npm run dev"

# Clean up
cd backend
rm -rf .venv db.sqlite3
cd ../frontend
rm -rf node_modules package-lock.json

# Restart
cd ..
./start.sh
```

#### Check System Status
```bash
# Check if services are running
ps aux | grep -E "(python|node)"

# Check ports
netstat -an | grep -E "(8000|5173)"

# Check disk space
df -h
```

## Getting Help

### 1. Check Logs
- Backend: Check terminal output
- Frontend: Check browser console (F12)
- Database: Check Django admin interface

### 2. Verify Configuration
- Check `rules/rules.yaml` for configuration issues
- Verify environment variables
- Check file permissions

### 3. Test Components
```bash
# Test backend API
curl http://localhost:8000/api/departments/

# Test frontend
curl http://localhost:5173/

# Test database
python manage.py shell
>>> from elections.models import Department
>>> Department.objects.count()
```

### 4. Common Solutions
1. **Restart services** - Often fixes temporary issues
2. **Clear cache** - Browser cache, Python cache, Node modules
3. **Check ports** - Ensure no conflicts
4. **Verify dependencies** - All packages installed correctly
5. **Check permissions** - Files and directories accessible

### 5. When to Rebuild
- Major configuration changes
- Dependency updates
- Database schema changes
- Environment changes

## Still Having Issues?

1. Check the error messages carefully
2. Look at the logs for specific error details
3. Verify all prerequisites are installed
4. Try the reset everything approach
5. Check if the issue is environment-specific

Remember: Most issues are resolved by restarting services or clearing caches!

