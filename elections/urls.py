from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import auth_views

router = DefaultRouter()
router.register(r'faculties', views.FacultyViewSet)
router.register(r'departments', views.DepartmentViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'delegates', views.DelegateViewSet)
router.register(r'rules', views.RuleViewSet)
router.register(r'snapshots', views.SnapshotViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/login/', auth_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', auth_views.register_user, name='register_user'),
    path('auth/logout/', auth_views.logout_user, name='logout_user'),
    path('auth/profile/', auth_views.get_user_profile, name='get_user_profile'),
    path('auth/profile/update/', auth_views.update_user_profile, name='update_user_profile'),
    
    # Dashboard
    path('dashboard/stats/', views.DashboardStatsView.as_view(), name='dashboard_stats'),
    
    # Course search endpoints
    path('courses/search/', views.CourseSearchView.as_view(), name='search_courses'),
    path('courses/all/', views.GetAllCoursesView.as_view(), name='get_all_courses'),
]
