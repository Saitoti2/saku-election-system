#!/usr/bin/env python
"""
Script to create a test user for SAKU Election Platform
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from elections.models import UserProfile, Course, Department, Faculty

def create_test_user():
    """Create a test user with complete profile"""
    
    # Create or get a course (get the first available course)
    try:
        course = Course.objects.first()
        if not course:
            print("No courses found. Please run the seed script first.")
            return
    except Exception as e:
        print(f"Error getting course: {e}")
        return
    
    username = 'test_student'
    email = 'test@kca.ac.ke'
    password = 'test123'
    
    # Delete existing test user if it exists
    if User.objects.filter(username=username).exists():
        User.objects.filter(username=username).delete()
        print(f"Deleted existing test user '{username}'")
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name='John',
        last_name='Doe'
    )
    
    # Create user profile
    profile = UserProfile.objects.create(
        user=user,
        user_type='ASPIRANT',
        full_name='John Doe',
        gender='Male',
        student_id='KCU/2023/TEST001',
        year_of_study=3,
        whatsapp_number='+254700000001',
        phone_number='+254700000001',
        course=course,
        council_position='CHAIR',
        vetting_status='PENDING'
    )
    
    print(f"Test user created successfully!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Registration Number: {profile.student_id}")
    print(f"Full Name: {profile.full_name}")
    print(f"Course: {course.name}")
    print(f"Department: {course.department.name}")
    print(f"Faculty: {course.department.faculty.name}")
    print(f"User Type: {profile.user_type}")
    print(f"Council Position: {profile.council_position}")

if __name__ == '__main__':
    create_test_user()
