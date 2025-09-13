#!/usr/bin/env python
"""
Script to create Saitoti admin user for SAKU Election Platform
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def create_saitoti_admin():
    """Create Saitoti admin user"""
    username = 'Saitoti'
    email = 'saitoti@saku.com'
    password = 'Saitoti2004'
    
    # Delete existing Saitoti user if it exists
    if User.objects.filter(username=username).exists():
        User.objects.filter(username=username).delete()
        print(f"Deleted existing user '{username}'")
    
    # Create superuser
    admin_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print(f"✅ Saitoti admin user created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Admin Status: {admin_user.is_staff}")
    print(f"Superuser Status: {admin_user.is_superuser}")

if __name__ == '__main__':
    create_saitoti_admin()
