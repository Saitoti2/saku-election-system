#!/usr/bin/env python
"""
Script to create admin user for SAKU Election Platform
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    """Create admin user if it doesn't exist"""
    username = 'admin'
    email = 'admin@saku.com'
    password = 'admin123'  # Change this in production!
    
    if User.objects.filter(username=username).exists():
        print(f"Admin user '{username}' already exists.")
        return
    
    # Create superuser
    admin_user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    print(f"Admin user created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print("\n⚠️  IMPORTANT: Change the password in production!")

if __name__ == '__main__':
    create_admin_user()
