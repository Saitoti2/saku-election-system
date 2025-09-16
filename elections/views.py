from rest_framework import viewsets, filters, decorators, response, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.db.models import Q
from .models import Faculty, Department, Course, Delegate, UserProfile, Rule, Snapshot
from .serializers import (
    FacultySerializer, DepartmentSerializer, CourseSerializer, DelegateSerializer,
    UserProfileSerializer, UserProfileCreateSerializer, RuleSerializer, SnapshotSerializer,
    LoginSerializer, RegisterSerializer, VerifyUserSerializer
)
from .whatsapp_service import whatsapp_service


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticated]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('faculty').all().order_by('name')
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'faculty__name']
    ordering_fields = ['name', 'code']


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('department', 'department__faculty').all().order_by('name')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code', 'department__name', 'department__faculty__name']
    ordering_fields = ['name', 'code']


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user', 'faculty', 'department', 'course').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'student_id', 'user__username', 'email']
    ordering_fields = ['created_at', 'full_name', 'student_id']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserProfileCreateSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['get'])
    def aspirants(self, request):
        """Get all council aspirants"""
        aspirants = self.queryset.filter(user_type='ASPIRANT')
        serializer = self.get_serializer(aspirants, many=True)
        return response.Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_verification(self, request):
        """Get profiles pending verification"""
        pending = self.queryset.filter(vetting_status='NOT_STARTED')
        serializer = self.get_serializer(pending, many=True)
        return response.Response(serializer.data)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a user profile"""
        profile = self.get_object()
        serializer = VerifyUserSerializer(data=request.data)
        
        if serializer.is_valid():
            profile.vetting_status = serializer.validated_data['vetting_status']
            profile.is_qualified = serializer.validated_data['is_qualified']
            profile.verification_notes = serializer.validated_data.get('verification_notes', '')
            profile.verified_by = request.user
            profile.verified_at = timezone.now()
            profile.save()
            
            # Send WhatsApp notification
            try:
                whatsapp_service.send_verification_notification(profile)
            except Exception as e:
                print(f"WhatsApp notification failed: {e}")
            
            return response.Response({'message': 'Profile verified successfully'})
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def send_whatsapp_notification(self, request, pk=None):
        """Manually send WhatsApp notification"""
        profile = self.get_object()
        try:
            whatsapp_service.send_verification_notification(profile)
            return response.Response({'message': 'WhatsApp notification sent successfully'})
        except Exception as e:
            return response.Response(
                {'error': f'Failed to send notification: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DelegateViewSet(viewsets.ModelViewSet):
    queryset = Delegate.objects.select_related('department', 'course').all()
    serializer_class = DelegateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'student_id', 'department__name']
    ordering_fields = ['created_at', 'full_name', 'student_id']

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a delegate"""
        delegate = self.get_object()
        serializer = VerifyUserSerializer(data=request.data)
        
        if serializer.is_valid():
            delegate.vetting_status = serializer.validated_data['vetting_status']
            delegate.is_qualified = serializer.validated_data['is_qualified']
            delegate.notes = serializer.validated_data.get('verification_notes', '')
            delegate.save()
            
            return response.Response({'message': 'Delegate verified successfully'})
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class SnapshotViewSet(viewsets.ModelViewSet):
    queryset = Snapshot.objects.all().order_by('-taken_at')
    serializer_class = SnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]


# Authentication Views
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                
                # Get user profile
                try:
                    profile = user.profile
                    profile_data = UserProfileSerializer(profile).data
                except UserProfile.DoesNotExist:
                    profile_data = None
                
                return response.Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                    },
                    'profile': profile_data
                })
            else:
                return response.Response(
                    {'error': 'Invalid credentials'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create user account
                user = User.objects.create_user(
                    username=serializer.validated_data['username'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password']
                )
                
                # Create user profile
                profile_data = serializer.validated_data.copy()
                profile_data.pop('username')
                profile_data.pop('password')
                profile_data.pop('email')
                
                profile = UserProfile.objects.create(
                    user=user,
                    email=serializer.validated_data['email'],
                    **profile_data
                )
                
                # Send admin notification
                try:
                    whatsapp_service.send_admin_registration_alert(profile)
                except Exception as e:
                    print(f"Admin notification failed: {e}")
                
                return response.Response({
                    'message': 'Registration successful',
                    'profile_id': profile.id
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return response.Response(
                    {'error': f'Registration failed: {str(e)}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    permission_classes = [permissions.IsAuthenticated]


class SnapshotViewSet(viewsets.ModelViewSet):
    queryset = Snapshot.objects.all().order_by('-taken_at')
    serializer_class = SnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]


# Dashboard Views
class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        stats = {
            'total_users': UserProfile.objects.count(),
            'total_aspirants': UserProfile.objects.filter(user_type='ASPIRANT').count(),
            'total_delegates': Delegate.objects.count(),
            'pending_verification': UserProfile.objects.filter(vetting_status='NOT_STARTED').count(),
            'qualified_aspirants': UserProfile.objects.filter(user_type='ASPIRANT', is_qualified=True).count(),
            'qualified_delegates': Delegate.objects.filter(is_qualified=True).count(),
        }
        return response.Response(stats)


class CourseSearchView(APIView):
    """
    Search courses by name with autocomplete functionality
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return response.Response({
                'courses': [],
                'message': 'Please enter at least 2 characters to search'
            })
        
        # Search courses by name (case-insensitive)
        courses = Course.objects.filter(
            Q(name__icontains=query)
        ).select_related('department', 'department__faculty')[:10]  # Limit to 10 results
        
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
        
        return response.Response({
            'courses': courses_data,
            'query': query,
            'count': len(courses_data)
        })


class GetAllCoursesView(APIView):
    """
    Get all courses for dropdown/selection
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        courses = Course.objects.select_related('department', 'department__faculty').all()
        
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
        
        return response.Response({
            'courses': courses_data,
            'count': len(courses_data)
        })