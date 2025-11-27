from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os


class Faculty(models.Model):
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Faculties"


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments", null=True, blank=True)
    code = models.SlugField(unique=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        if self.faculty:
            return f"{self.name} ({self.faculty.name})"
        return self.name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.name}"

    @property
    def faculty(self):
        if self.department and self.department.faculty:
            return self.department.faculty
        return None


class VettingStatus(models.TextChoices):
    NOT_STARTED = "NOT_STARTED", "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    PASSED = "PASSED", "PASSED"
    FAILED = "FAILED", "FAILED"


class Gender(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    OTHER = "Other", "Other"


class UserType(models.TextChoices):
    STUDENT = "STUDENT", "Student"
    ASPIRANT = "ASPIRANT", "Council Aspirant"
    DELEGATE = "DELEGATE", "Delegate"
    IECK = "IECK", "IECK Member"
    ADMIN = "ADMIN", "Admin"


class CouncilPosition(models.TextChoices):
    CHAIR = "CHAIR", "Chair (President)"
    VICE_CHAIR = "VICE_CHAIR", "Vice Chair"
    SECRETARY_GENERAL = "SECRETARY_GENERAL", "Secretary General"
    FINANCE_SECRETARY = "FINANCE_SECRETARY", "Finance Secretary"
    ACADEMIC_SECRETARY = "ACADEMIC_SECRETARY", "Academic Secretary"
    SPORTS_SECRETARY = "SPORTS_SECRETARY", "Sports Secretary"
    SPECIAL_INTERESTS_SECRETARY = "SPECIAL_INTERESTS_SECRETARY", "Special Interests Secretary"


def user_document_upload_path(instance, filename):
    """Generate upload path for user documents"""
    return f"documents/{instance.user_type}/{instance.student_id}/{filename}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    user_type = models.CharField(max_length=20, choices=UserType.choices)
    
    # Basic Information
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    student_id = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="users", null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="users", null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    year_of_study = models.PositiveSmallIntegerField()
    whatsapp_number = models.CharField(max_length=20)
    
    # For Aspirants - Position they're running for
    council_position = models.CharField(max_length=50, choices=CouncilPosition.choices, blank=True, null=True)
    
    # Contact Information
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    # Document Uploads
    school_fees_screenshot = models.ImageField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text="Screenshot showing 80%+ school fees clearance"
    )
    last_semester_results = models.FileField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Last semester results (PDF)"
    )
    second_last_semester_results = models.FileField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Second last semester results (PDF)"
    )
    course_registration_screenshot = models.ImageField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text="Current semester course registration screenshot"
    )
    good_conduct_certificate = models.FileField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Certificate of Good Conduct (PDF)"
    )
    school_id_image = models.ImageField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        help_text="School ID image"
    )
    last_semester_transcript = models.FileField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Last semester transcript (PDF)"
    )
    second_last_semester_transcript = models.FileField(
        upload_to=user_document_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Second last semester transcript (PDF)"
    )
    
    # Verification Status
    vetting_status = models.CharField(max_length=20, choices=VettingStatus.choices, default=VettingStatus.NOT_STARTED)
    is_qualified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_profiles")
    verified_at = models.DateTimeField(null=True, blank=True)
    
    # WhatsApp Notification
    whatsapp_notification_sent = models.BooleanField(default=False)
    whatsapp_notification_sent_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.student_id}) - {self.get_user_type_display()}"

    class Meta:
        ordering = ['-created_at']


class Delegate(models.Model):
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="delegates")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    year_of_study = models.PositiveSmallIntegerField()
    student_id = models.CharField(max_length=50, unique=True)
    contacts = models.JSONField(default=dict)
    vetting_status = models.CharField(max_length=20, choices=VettingStatus.choices, default=VettingStatus.NOT_STARTED)
    eligibility = models.JSONField(default=dict)
    is_qualified = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.full_name} ({self.student_id})"


class Rule(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    citation = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.key


class Snapshot(models.Model):
    taken_at = models.DateTimeField(auto_now_add=True)
    totals = models.JSONField()

    def __str__(self) -> str:
        return f"Snapshot {self.taken_at}"
