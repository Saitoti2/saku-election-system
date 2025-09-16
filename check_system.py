#!/usr/bin/env python
"""
System check script to verify all components are working properly
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def check_system():
    print("🔍 Running system checks...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    from django.db import connection
    from django.contrib.auth import get_user_model
    from django.core.management import call_command
    
    # Check database connection
    print("📊 Checking database connection...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection: OK")
    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
        return False
    
    # Check if auth_user table exists
    print("👤 Checking auth_user table...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user'")
            if cursor.fetchone():
                print("✅ auth_user table: EXISTS")
            else:
                print("❌ auth_user table: MISSING")
                return False
    except Exception as e:
        print(f"❌ auth_user table check: FAILED - {e}")
        return False
    
    # Check if superuser exists
    print("🔑 Checking superuser...")
    try:
        User = get_user_model()
        if User.objects.filter(username='admin').exists():
            print("✅ Superuser: EXISTS")
        else:
            print("⚠️  Superuser: MISSING - Creating...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser: CREATED")
    except Exception as e:
        print(f"❌ Superuser check: FAILED - {e}")
        return False
    
    # Check elections app tables
    print("🗳️  Checking elections app tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            election_tables = [t for t in tables if 'elections_' in t]
            if election_tables:
                print(f"✅ Elections tables: {len(election_tables)} found")
            else:
                print("⚠️  Elections tables: MISSING")
    except Exception as e:
        print(f"❌ Elections tables check: FAILED - {e}")
    
    print("🎉 System check completed!")
    return True

if __name__ == '__main__':
    success = check_system()
    sys.exit(0 if success else 1)
