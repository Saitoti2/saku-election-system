#!/usr/bin/env python
"""
Deployment script for Render
This script ensures everything is set up correctly
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def main():
    print("🚀 Starting SAKU Election System deployment...")
    
    # Set up Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    from django.contrib.auth import get_user_model
    
    try:
        # 1. Check if database file exists
        db_path = os.path.join(os.getcwd(), 'db.sqlite3')
        print(f"📁 Database path: {db_path}")
        print(f"📁 Database exists: {os.path.exists(db_path)}")
        
        # 2. Run migrations with force
        print("📊 Running database migrations...")
        call_command('migrate', '--run-syncdb', verbosity=2)
        print("✅ Migrations completed")
        
        # 3. Verify database tables
        print("🔍 Verifying database tables...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Found {len(tables)} tables: {', '.join(tables)}")
            
            # Check if auth_user table exists
            if 'auth_user' in tables:
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                user_count = cursor.fetchone()[0]
                print(f"✅ auth_user table exists with {user_count} users")
            else:
                print("❌ auth_user table missing!")
                return False
        
        # 4. Create superuser if needed
        print("👤 Checking superuser...")
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            print("Creating superuser...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print("✅ Superuser created: admin/admin123")
        else:
            print("✅ Superuser already exists")
        
        # 5. Collect static files
        print("📁 Collecting static files...")
        call_command('collectstatic', '--noinput', verbosity=2)
        print("✅ Static files collected")
        
        # 6. Final verification
        print("🔍 Final system check...")
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            user_count = cursor.fetchone()[0]
            print(f"✅ Final check: {user_count} users in database")
        
        print("🎉 Deployment setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
