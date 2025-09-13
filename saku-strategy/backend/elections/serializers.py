from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Faculty, Department, Course, Delegate, UserProfile, 
    UserType, CouncilPosition, VettingStatus
)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'code', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), source='faculty', write_only=True
    )

    class Meta:
        model = Department
        fields = ['id', 'code', 'name', 'faculty', 'faculty_id']


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    faculty_name = serializers.CharField(source='department.faculty.name', read_only=True, allow_null=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'department_name', 'faculty_name']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    council_position_display = serializers.CharField(source='get_council_position_display', read_only=True)
    vetting_status_display = serializers.CharField(source='get_vetting_status_display', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.get_full_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at', 'verified_by', 'verified_at', 
                           'whatsapp_notification_sent', 'whatsapp_notification_sent_at']


class UserProfileCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = UserProfile
        exclude = ['user', 'verified_by', 'verified_at', 'whatsapp_notification_sent', 
                  'whatsapp_notification_sent_at', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        # Get course and automatically assign faculty and department
        course = validated_data.get('course')
        if course:
            validated_data['department'] = course.department
            validated_data['faculty'] = course.department.faculty
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=validated_data.get('full_name', '').split()[0] if validated_data.get('full_name') else '',
            last_name=' '.join(validated_data.get('full_name', '').split()[1:]) if len(validated_data.get('full_name', '').split()) > 1 else ''
        )
        
        # Create profile
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile


class UserSignupSerializer(serializers.ModelSerializer):
    """Simplified serializer for basic user signup without election documents"""
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )
    
    # Make document fields optional
    school_fees_screenshot = serializers.ImageField(required=False, allow_null=True)
    last_semester_results = serializers.FileField(required=False, allow_null=True)
    second_last_semester_results = serializers.FileField(required=False, allow_null=True)
    course_registration_screenshot = serializers.ImageField(required=False, allow_null=True)
    good_conduct_certificate = serializers.FileField(required=False, allow_null=True)
    school_id_image = serializers.ImageField(required=False, allow_null=True)
    last_semester_transcript = serializers.FileField(required=False, allow_null=True)
    second_last_semester_transcript = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'password', 'user_type', 'full_name', 'gender', 
            'student_id', 'year_of_study', 'whatsapp_number', 'phone_number', 'course_id',
            'council_position',
            'school_fees_screenshot', 'last_semester_results', 'second_last_semester_results',
            'course_registration_screenshot', 'good_conduct_certificate', 'school_id_image',
            'last_semester_transcript', 'second_last_semester_transcript'
        ]

    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        # Get course and automatically assign faculty and department
        course = validated_data.get('course')
        if course:
            validated_data['department'] = course.department
            validated_data['faculty'] = course.department.faculty
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=validated_data.get('full_name', '').split()[0] if validated_data.get('full_name') else '',
            last_name=' '.join(validated_data.get('full_name', '').split()[1:]) if len(validated_data.get('full_name', '').split()) > 1 else ''
        )
        
        # Set default values for election-related fields
        validated_data['user_type'] = validated_data.get('user_type', 'STUDENT')
        validated_data['vetting_status'] = 'NOT_STARTED'
        validated_data['is_qualified'] = False
        
        # Create profile
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile


class DelegateSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True
    )
    course = CourseSerializer(read_only=True)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source='course', write_only=True
    )

    class Meta:
        model = Delegate
        fields = [
            'id','full_name','gender','year_of_study','student_id','contacts','vetting_status',
            'eligibility','is_qualified','notes','created_at','department','department_id','course','course_id'
        ]
        read_only_fields = ['eligibility','is_qualified','created_at']



