from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Faculty, Department, UserProfile, Election, Candidate, Vote

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    
    class Meta:
        model = Department
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user_type', 'student_id', 'phone_number', 'department', 'is_verified', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

class ElectionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Election
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    votes_received = serializers.ReadOnlyField()
    
    class Meta:
        model = Candidate
        fields = '__all__'

class VoteSerializer(serializers.ModelSerializer):
    voter = UserSerializer(read_only=True)
    candidate = CandidateSerializer(read_only=True)
    
    class Meta:
        model = Vote
        fields = '__all__'
