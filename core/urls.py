from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
import os

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        "status": "healthy", 
        "message": "SAKU Election System is running"
    })

def serve_frontend_file(request, filename):
    """Serve frontend HTML files"""
    frontend_path = os.path.join(settings.BASE_DIR, 'frontend', filename)
    try:
        with open(frontend_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html')
    except FileNotFoundError:
        return HttpResponse("File not found", status=404)

# URL patterns
urlpatterns = [
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('elections.urls')),
    
    # Frontend pages
    path('login/', lambda r: serve_frontend_file(r, 'login-fixed.html')),
    path('admin-dashboard/', lambda r: serve_frontend_file(r, 'admin-dashboard-enhanced.html')),
    path('register/', lambda r: serve_frontend_file(r, 'election-registration.html')),
    path('portal/', lambda r: serve_frontend_file(r, 'personal-portal.html')),
    path('verify/', lambda r: serve_frontend_file(r, 'student-verification.html')),
    path('signup-complete/', lambda r: serve_frontend_file(r, 'signup-complete.html')),
    path('home/', lambda r: serve_frontend_file(r, 'index.html')),
    path('index/', lambda r: serve_frontend_file(r, 'index.html')),
]

# Serve static files
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
