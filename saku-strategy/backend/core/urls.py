"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView
import os
from . import test_pages

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
        "message": "Saku Election System is running",
        "port": os.getenv('PORT', '8000'),
        "debug": os.getenv('DEBUG', 'False'),
        "database": db_status
    })

def serve_frontend_file(request, filename):
    """Serve frontend HTML files"""
    frontend_path = os.path.join(settings.BASE_DIR, '..', 'frontend', filename)
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

    # Test pages for debugging
    path('test-db/', test_pages.test_database, name='test_database'),
    path('test-auth/', test_pages.test_auth, name='test_auth'),

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
