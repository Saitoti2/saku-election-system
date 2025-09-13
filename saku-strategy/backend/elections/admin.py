from django.contrib import admin
from .models import Faculty, Department, Course, Delegate, UserProfile, Rule, Snapshot


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'faculty']
    list_filter = ['faculty']
    search_fields = ['code', 'name', 'faculty__name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'faculty']
    list_filter = ['department', 'department__faculty']
    search_fields = ['name', 'department__name', 'department__faculty__name']


@admin.register(Delegate)
class DelegateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'department', 'course', 'vetting_status', 'is_qualified']
    list_filter = ['department', 'course', 'vetting_status', 'is_qualified', 'gender']
    search_fields = ['full_name', 'student_id', 'department__name', 'course__name']
    readonly_fields = ['created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'user_type', 'council_position', 'faculty', 'department', 'vetting_status', 'is_qualified']
    list_filter = ['user_type', 'council_position', 'faculty', 'department', 'vetting_status', 'is_qualified', 'gender']
    search_fields = ['full_name', 'student_id', 'faculty__name', 'department__name', 'course__name', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'verified_at', 'whatsapp_notification_sent_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'user_type', 'full_name', 'gender', 'student_id', 'faculty', 'department', 'course', 'year_of_study')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_number', 'whatsapp_number')
        }),
        ('Council Position', {
            'fields': ('council_position',),
            'classes': ('collapse',)
        }),
        ('Documents', {
            'fields': (
                'school_fees_screenshot', 'last_semester_results', 'second_last_semester_results',
                'course_registration_screenshot', 'good_conduct_certificate', 'school_id_image',
                'last_semester_transcript', 'second_last_semester_transcript'
            ),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('vetting_status', 'is_qualified', 'verification_notes', 'verified_by', 'verified_at')
        }),
        ('Notifications', {
            'fields': ('whatsapp_notification_sent', 'whatsapp_notification_sent_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ['key', 'citation']
    search_fields = ['key', 'citation']


@admin.register(Snapshot)
class SnapshotAdmin(admin.ModelAdmin):
    list_display = ['taken_at']
    readonly_fields = ['taken_at']
