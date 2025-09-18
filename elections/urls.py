from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'elections', views.ElectionViewSet)
router.register(r'candidates', views.CandidateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/verify/', views.VerifyUserView.as_view(), name='verify'),
    path('vote/', views.VoteView.as_view(), name='vote'),
    path('results/<int:election_id>/', views.ElectionResultsView.as_view(), name='results'),
]
