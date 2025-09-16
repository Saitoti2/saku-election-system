from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Faculty, Department, Course, UserProfile, Delegate, Rule, Snapshot,
    UserType, CouncilPosition, VettingStatus, Gender
)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'code', 'name']


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Department
        fields = ['id', 'code', 'name', 'faculty', 'faculty_id']


class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    faculty = FacultySerializer(source='department.faculty', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'department', 'department_id', 'faculty']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    faculty = FacultySerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    
    # Foreign key IDs for writing
    faculty_id = serializers.IntegerField(write_only=True, required=False)
    department_id = serializers.IntegerField(write_only=True, required=False)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_type', 'full_name', 'gender', 'student_id',
            'faculty', 'department', 'course', 'year_of_study', 'whatsapp_number',
            'council_position', 'email', 'phone_number',
            'school_fees_screenshot', 'last_semester_results', 'second_last_semester_results',
            'course_registration_screenshot', 'good_conduct_certificate', 'school_id_image',
            'last_semester_transcript', 'second_last_semester_transcript',
            'vetting_status', 'is_qualified', 'verification_notes', 'verified_by', 'verified_at',
            'whatsapp_notification_sent', 'whatsapp_notification_sent_at',
            'created_at', 'updated_at',
            'faculty_id', 'department_id', 'course_id'
        ]
        read_only_fields = ['created_at', 'updated_at', 'verified_by', 'verified_at']


class UserProfileCreateSerializer(serializers.ModelSerializer):
    # User account fields
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    
    # Foreign key IDs
    faculty_id = serializers.IntegerField(required=False)
    department_id = serializers.IntegerField(required=False)
    course_id = serializers.IntegerField()

    class Meta:
        model = UserProfile
        fields = [
            'username', 'password', 'email', 'user_type', 'full_name', 'gender', 'student_id',
            'faculty_id', 'department_id', 'course_id', 'year_of_study', 'whatsapp_number',
            'council_position', 'phone_number',
            'school_fees_screenshot', 'last_semester_results', 'second_last_semester_results',
            'course_registration_screenshot', 'good_conduct_certificate', 'school_id_image',
            'last_semester_transcript', 'second_last_semester_transcript'
        ]

    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        
        # Create user account
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create user profile
        profile = UserProfile.objects.create(
            user=user,
            email=email,
            **validated_data
        )
        
        return profile


class DelegateSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    department_id = serializers.IntegerField(write_only=True)
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Delegate
        fields = [
            'id', 'full_name', 'gender', 'department', 'course', 'year_of_study',
            'student_id', 'contacts', 'vetting_status', 'eligibility', 'is_qualified',
            'notes', 'created_at', 'department_id', 'course_id'
        ]
        read_only_fields = ['created_at']


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'key', 'value', 'citation']


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ['id', 'taken_at', 'totals']


# Authentication serializers
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8)
    email = serializers.EmailField()
    user_type = serializers.ChoiceField(choices=UserType.choices)
    full_name = serializers.CharField(max_length=255)
    gender = serializers.ChoiceField(choices=Gender.choices)
    student_id = serializers.CharField(max_length=50)
    faculty_id = serializers.IntegerField(required=False)
    department_id = serializers.IntegerField(required=False)
    course_id = serializers.IntegerField()
    year_of_study = serializers.IntegerField()
    whatsapp_number = serializers.CharField(max_length=20)
    council_position = serializers.ChoiceField(choices=CouncilPosition.choices, required=False)
    phone_number = serializers.CharField(max_length=20)


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
        from django.contrib.auth.models import User
        
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


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'key', 'value', 'citation']


class SnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snapshot
        fields = ['id', 'taken_at', 'totals']


class VerifyUserSerializer(serializers.Serializer):
    vetting_status = serializers.ChoiceField(choices=VettingStatus.choices)
    is_qualified = serializers.BooleanField()
    verification_notes = serializers.CharField(required=False, allow_blank=True)
