"""
Authentication views for SAKU Election Platform
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer
import json


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that returns user profile data along with tokens
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user from request
            username = request.data.get('username')
            password = request.data.get('password')
            
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    try:
                        # Get user profile
                        profile = UserProfile.objects.get(user=user)
                        profile_data = UserProfileSerializer(profile).data
                        
                        # Add profile data to response
                        response.data['profile'] = profile_data
                        response.data['user_type'] = profile.user_type
                        response.data['is_admin'] = user.is_staff
                        
                    except UserProfile.DoesNotExist:
                        # If no profile exists, create basic user data
                        response.data['profile'] = {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                        }
                        response.data['user_type'] = 'STUDENT'
                        response.data['is_admin'] = user.is_staff
        
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and create their profile
    """
    try:
        data = request.data
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'student_id', 'whatsapp_number', 'phone_number', 'gender', 'year_of_study', 'course_id']
        for field in required_fields:
            if not data.get(field):
                return Response({
                    'error': f'{field} is required'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already exists
        if User.objects.filter(username=data['username']).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=data['email']).exists():
            return Response({
                'error': 'Email already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Prepare profile data for serializer
        profile_data = {
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],
            'user_type': data.get('user_type', 'STUDENT'),
            'full_name': data['full_name'],
            'gender': data['gender'],
            'student_id': data['student_id'],
            'year_of_study': data['year_of_study'],
            'whatsapp_number': data['whatsapp_number'],
            'phone_number': data['phone_number'],
            'course_id': data['course_id'],
            'council_position': data.get('council_position'),
        }
        
        # Add file uploads if provided (optional for signup)
        file_fields = [
            'school_fees_screenshot', 'last_semester_results', 'second_last_semester_results',
            'course_registration_screenshot', 'good_conduct_certificate', 'school_id_image',
            'last_semester_transcript', 'second_last_semester_transcript'
        ]
        
        for field in file_fields:
            if field in request.FILES:
                profile_data[field] = request.FILES[field]
        
        from .serializers import UserSignupSerializer
        serializer = UserSignupSerializer(data=profile_data)
        
        if serializer.is_valid():
            profile = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(profile.user)
            access_token = refresh.access_token
            
            # Get profile data for response
            profile_serializer = UserProfileSerializer(profile)
            
            # Send WhatsApp notification to admin for new registrations (except basic STUDENT signups)
            if profile.user_type != 'STUDENT':
                try:
                    from .whatsapp_service import WhatsAppService
                    from django.conf import settings
                    
                    whatsapp_service = WhatsAppService()
                    admin_phone = getattr(settings, 'ADMIN_PHONE_NUMBER', '+254769582779')
                    
                    # Send admin notification
                    whatsapp_service.send_admin_registration_alert(
                        admin_phone=admin_phone,
                        student_name=profile.full_name,
                        reg_number=profile.student_id,
                        user_type=profile.user_type,
                        position=profile.council_position
                    )
                    
                    print(f"✅ WhatsApp notification sent for {profile.full_name} ({profile.student_id})")
                    
                except Exception as e:
                    print(f"❌ WhatsApp notification failed: {e}")
            
            return Response({
                'message': 'User registered successfully',
                'access': str(access_token),
                'refresh': str(refresh),
                'profile': profile_serializer.data,
                'user_type': profile.user_type,
                'is_admin': profile.user.is_staff
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': 'Profile creation failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'error': 'Registration failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """
    Refresh JWT token
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        
        return Response({
            'access': str(access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Token refresh failed',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Logout user by blacklisting the refresh token
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Logout failed',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user's profile
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        
        return Response({
            'profile': serializer.data,
            'user_type': profile.user_type,
            'is_admin': request.user.is_staff
        }, status=status.HTTP_200_OK)
        
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Failed to get profile',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    """
    Update current user's profile
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Profile update failed',
                'details': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': 'Failed to update profile',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
