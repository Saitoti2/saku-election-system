from rest_framework import viewsets, filters, decorators, response, status, permissions
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Faculty, Department, Course, Delegate, UserProfile
from .serializers import (
    FacultySerializer, DepartmentSerializer, CourseSerializer, DelegateSerializer,
    UserProfileSerializer, UserProfileCreateSerializer
)
from .whatsapp_service import whatsapp_service
from rules_engine.loader import load_rules
from rules_engine.validator import validate_delegate


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all().order_by('name')
    serializer_class = FacultySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.select_related('faculty').all().order_by('name')
    serializer_class = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('department', 'department__faculty').all().order_by('name')
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search courses with autocomplete functionality"""
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return response.Response([])
        
        courses = self.queryset.filter(name__icontains=query)[:10]
        serializer = self.get_serializer(courses, many=True)
        return response.Response(serializer.data)


class DelegateViewSet(viewsets.ModelViewSet):
    queryset = Delegate.objects.select_related('department','course').all().order_by('-created_at')
    serializer_class = DelegateSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name','student_id','department__name','course__name']

    def perform_create(self, serializer):
        instance = serializer.save()
        rules = load_rules()
        verdict = validate_delegate(instance, rules)
        instance.eligibility = verdict
        instance.is_qualified = bool(verdict.get('overall_passed'))
        instance.save(update_fields=['eligibility','is_qualified'])

    @decorators.action(detail=False, methods=['get'])
    def metrics(self, request):
        # Basic coverage metrics per department
        departments = Department.objects.all()
        metrics_data = []
        
        for dept in departments:
            total_candidates = Delegate.objects.filter(department=dept).count()
            qualified = Delegate.objects.filter(department=dept, is_qualified=True).count()
            target_min = 3  # Minimum delegates per department
            
            # Gender distribution
            male_count = Delegate.objects.filter(department=dept, gender='Male').count()
            female_count = Delegate.objects.filter(department=dept, gender='Female').count()
            
            metrics_data.append({
                'department': dept.name,
                'code': dept.code,
                'total_candidates': total_candidates,
                'qualified': qualified,
                'target_min': target_min,
                'gap_to_min': max(0, target_min - qualified),
                'female': female_count,
                'male': male_count,
                'gender_ratio_female': female_count / max(1, total_candidates),
                'gender_target_female': 0.33,  # 33% target
                'gender_gap': max(0, 0.33 - (female_count / max(1, total_candidates)))
            })
        
        # Calculate overall score
        total_gap = sum(dept['gap_to_min'] for dept in metrics_data)
        total_gender_gap = sum(dept['gender_gap'] for dept in metrics_data)
        score = max(0, 100 - (total_gap * 5) - (total_gender_gap * 20))
        
        return response.Response({
            'departments': metrics_data,
            'score': {'score': score, 'components': {
                'min_gap_sum': total_gap,
                'gender_gap_sum': total_gender_gap,
                'buffer_sum': 0,
                'weights': {'w_min_gap': 5.0, 'w_gender_gap': 20.0, 'w_buffer': 2.0}
            }}
        })



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user', 'department', 'course', 'verified_by').all().order_by('-created_at')
    serializer_class = UserProfileSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['full_name', 'student_id', 'department__name', 'course__name', 'user_type']
    ordering_fields = ['created_at', 'full_name', 'vetting_status']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserProfileCreateSerializer
        return UserProfileSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]  # Allow registration without authentication
        elif self.action in ['list']:
            permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can list
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filter queryset based on user permissions
        """
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                # Admin can see all profiles
                return UserProfile.objects.select_related('user', 'department', 'course', 'verified_by').all().order_by('-created_at')
            else:
                # Students can only see their own profile
                return UserProfile.objects.filter(user=self.request.user).select_related('user', 'department', 'course', 'verified_by').order_by('-created_at')
        else:
            # Unauthenticated users see nothing
            return UserProfile.objects.none()

    def create(self, request, *args, **kwargs):
        """Create a new user profile and send admin notification"""
        from django.conf import settings
        
        response = super().create(request, *args, **kwargs)
        
        # Send admin notification if profile was created successfully
        if response.status_code == 201:
            profile_data = response.data
            admin_phone = getattr(settings, 'ADMIN_PHONE_NUMBER', '+254700000000')
            
            # Send WhatsApp notification to admin
            whatsapp_service.send_admin_registration_alert(
                admin_phone=admin_phone,
                student_name=profile_data.get('full_name', 'Unknown'),
                reg_number=profile_data.get('student_id', 'Unknown'),
                user_type=profile_data.get('user_type', 'Unknown'),
                position=profile_data.get('council_position')
            )
        
        return response

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a user profile (Admin only)"""
        if not request.user.is_staff:
            return response.Response({
                'error': 'Only administrators can verify profiles'
            }, status=403)
        
        profile = self.get_object()
        is_qualified = request.data.get('is_qualified', False)
        verification_notes = request.data.get('verification_notes', '')
        
        profile.vetting_status = 'PASSED' if is_qualified else 'FAILED'
        profile.is_qualified = is_qualified
        profile.verification_notes = verification_notes
        profile.verified_by = request.user
        profile.verified_at = timezone.now()
        profile.save()
        
        # Send WhatsApp notification
        if not profile.whatsapp_notification_sent:
            if is_qualified:
                success = whatsapp_service.send_qualification_notification(
                    phone_number=profile.whatsapp_number,
                    full_name=profile.full_name,
                    position=profile.get_council_position_display() if profile.council_position else None
                )
            else:
                success = whatsapp_service.send_rejection_notification(
                    phone_number=profile.whatsapp_number,
                    full_name=profile.full_name,
                    reason=verification_notes
                )
            
            if success:
                profile.whatsapp_notification_sent = True
                profile.whatsapp_notification_sent_at = timezone.now()
                profile.save()
        
        serializer = self.get_serializer(profile)
        return response.Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending_verification(self, request):
        """Get all profiles pending verification"""
        pending_profiles = self.queryset.filter(vetting_status='NOT_STARTED')
        serializer = self.get_serializer(pending_profiles, many=True)
        return response.Response(serializer.data)

    @action(detail=False, methods=['get'])
    def qualified(self, request):
        """Get all qualified profiles"""
        qualified_profiles = self.queryset.filter(is_qualified=True)
        serializer = self.get_serializer(qualified_profiles, many=True)
        return response.Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get profiles by user type"""
        user_type = request.query_params.get('type')
        if user_type:
            profiles = self.queryset.filter(user_type=user_type)
            serializer = self.get_serializer(profiles, many=True)
            return response.Response(serializer.data)
        return response.Response({'error': 'Type parameter required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get statistics about user profiles (Admin only)"""
        if not request.user.is_staff:
            return response.Response({
                'error': 'Only administrators can view statistics'
            }, status=403)
        total_profiles = self.queryset.count()
        qualified_profiles = self.queryset.filter(is_qualified=True).count()
        pending_profiles = self.queryset.filter(vetting_status='NOT_STARTED').count()
        
        # By user type
        aspirants = self.queryset.filter(user_type='ASPIRANT').count()
        delegates = self.queryset.filter(user_type='DELEGATE').count()
        ieck_members = self.queryset.filter(user_type='IECK').count()
        
        # By position (for aspirants)
        position_stats = {}
        for position_code, position_name in UserProfile._meta.get_field('council_position').choices:
            count = self.queryset.filter(user_type='ASPIRANT', council_position=position_code).count()
            if count > 0:
                position_stats[position_name] = count
        
        return response.Response({
            'total_profiles': total_profiles,
            'qualified_profiles': qualified_profiles,
            'pending_profiles': pending_profiles,
            'by_user_type': {
                'aspirants': aspirants,
                'delegates': delegates,
                'ieck_members': ieck_members
            },
            'by_position': position_stats
        })
    
    @action(detail=False, methods=['get'])
    def admin_all_profiles(self, request):
        """Get all profiles for admin dashboard (Admin only)"""
        if not request.user.is_staff:
            return response.Response({
                'error': 'Only administrators can view all profiles'
            }, status=403)
        
        # Admin can see all profiles regardless of queryset filtering
        all_profiles = UserProfile.objects.select_related('user', 'department', 'course', 'verified_by').all().order_by('-created_at')
        serializer = UserProfileSerializer(all_profiles, many=True)
        
        return response.Response({
            'profiles': serializer.data,
            'count': all_profiles.count()
        })


# Create your views here.
