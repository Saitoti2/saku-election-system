from django.contrib import admin
from .models import Faculty, Department, UserProfile, Election, Candidate, Vote

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['name', 'faculty__name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'student_id', 'phone_number', 'is_verified']
    list_filter = ['user_type', 'is_verified', 'department']
    search_fields = ['user__username', 'user__email', 'student_id', 'phone_number']

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date', 'created_by']
    list_filter = ['status', 'start_date', 'end_date']
    search_fields = ['title', 'description']

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['user', 'election', 'position', 'votes_received', 'is_approved']
    list_filter = ['election', 'position', 'is_approved']
    search_fields = ['user__username', 'position', 'manifesto']

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['voter', 'election', 'candidate', 'voted_at']
    list_filter = ['election', 'voted_at']
    search_fields = ['voter__username', 'candidate__user__username']
