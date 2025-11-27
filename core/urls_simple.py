from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
import os
<<<<<<< HEAD:saku-strategy/backend/core/urls.py
# from . import test_pages
=======
>>>>>>> 33ad9e5e2edb60aa24020e0c6b1ba9800aa868d5:core/urls_simple.py

def health_check(request):
    import os
    from django.db import connection
    
    # Test database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return JsonResponse({
        "status": "healthy", 
        "message": "SAKU Election System is running",
        "port": os.getenv('PORT', '8000'),
        "debug": os.getenv('DEBUG', 'False'),
        "database": db_status
    })

def serve_frontend_file(request, filename):
    """Serve frontend HTML files"""
    frontend_path = os.path.join(settings.BASE_DIR, 'frontend', filename)
    try:
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse(f"File {filename} not found", status=404)

urlpatterns = [
    path('', health_check, name='health_check'),
    path('api/', include('elections.urls')),
    path('admin/', admin.site.urls),
<<<<<<< HEAD:saku-strategy/backend/core/urls.py

    # Test pages for debugging
    # path('test-db/', test_pages.test_database, name='test_database'),
    # path('test-auth/', test_pages.test_auth, name='test_auth'),

=======
    
>>>>>>> 33ad9e5e2edb60aa24020e0c6b1ba9800aa868d5:core/urls_simple.py
    # Frontend pages
    path('login/', lambda r: serve_frontend_file(r, 'login-fixed.html'), name='login'),
    path('admin-dashboard/', lambda r: serve_frontend_file(r, 'admin-dashboard-enhanced.html'), name='admin_dashboard'),
    path('register/', lambda r: serve_frontend_file(r, 'election-registration.html'), name='register'),
    path('portal/', lambda r: serve_frontend_file(r, 'personal-portal.html'), name='portal'),
    path('verify/', lambda r: serve_frontend_file(r, 'student-verification.html'), name='verify'),
    path('signup-complete/', lambda r: serve_frontend_file(r, 'signup-complete.html'), name='signup_complete'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
