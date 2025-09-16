from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
import os

def health_check(request):
    """Health check endpoint"""
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
        "database": db_status,
        "debug": settings.DEBUG
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

def serve_login(request):
    return serve_frontend_file(request, 'login-fixed.html')

def serve_admin_dashboard(request):
    return serve_frontend_file(request, 'admin-dashboard-enhanced.html')

def serve_register(request):
    return serve_frontend_file(request, 'election-registration.html')

def serve_portal(request):
    return serve_frontend_file(request, 'personal-portal.html')

def serve_verify(request):
    return serve_frontend_file(request, 'student-verification.html')

def serve_signup_complete(request):
    return serve_frontend_file(request, 'signup-complete.html')

def serve_index(request):
    return serve_frontend_file(request, 'index.html')

def serve_test_dynamic(request):
    return serve_frontend_file(request, 'test-dynamic.html')

def serve_test_course_search(request):
    return serve_frontend_file(request, 'test-course-search.html')

def test_course_search(request):
    """Test endpoint for course search"""
    from elections.models import Course
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    
    # If no query or empty query, return all courses
    if not query:
        courses = Course.objects.select_related('department', 'department__faculty').all()
    elif len(query) < 2:
        return JsonResponse({
            'courses': [],
            'message': 'Please enter at least 2 characters to search'
        })
    else:
        # Search courses by name (case-insensitive)
        courses = Course.objects.filter(
            Q(name__icontains=query)
        ).select_related('department', 'department__faculty')[:10]
    
    # Format response data
    courses_data = []
    for course in courses:
        courses_data.append({
            'id': course.id,
            'name': course.name,
            'department': course.department.name,
            'faculty': course.department.faculty.name,
            'department_code': course.department.code,
            'faculty_code': course.department.faculty.code
        })
    
    return JsonResponse({
        'courses': courses_data,
        'query': query,
        'count': len(courses_data)
    })

urlpatterns = [
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('elections.urls')),

    # Frontend pages
    path('login/', serve_login, name='login'),
    path('admin-dashboard/', serve_admin_dashboard, name='admin_dashboard'),
    path('register/', serve_register, name='register'),
        path('portal/', serve_portal, name='portal'),
        path('verify/', serve_verify, name='verify'),
        path('signup-complete/', serve_signup_complete, name='signup_complete'),
        path('home/', serve_index, name='home'),
        path('index/', serve_index, name='index'),
        path('test-dynamic/', serve_test_dynamic, name='test_dynamic'),
        path('test-course-search/', serve_test_course_search, name='test_course_search'),
        
        # Course search endpoint
        path('search-courses/', test_course_search, name='test_course_search'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve frontend files as static files
    urlpatterns += static('/frontend/', document_root=os.path.join(settings.BASE_DIR, 'frontend'))