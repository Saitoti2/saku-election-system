from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import FacultyViewSet, DepartmentViewSet, CourseViewSet, DelegateViewSet, UserProfileViewSet
from . import auth_views

router = DefaultRouter()
router.register(r'faculties', FacultyViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'delegates', DelegateViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/login/', auth_views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', auth_views.register_user, name='register_user'),
    path('auth/logout/', auth_views.logout_user, name='logout_user'),
    path('auth/profile/', auth_views.get_user_profile, name='get_user_profile'),
    path('auth/profile/update/', auth_views.update_user_profile, name='update_user_profile'),
]


