from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Set up the database with migrations and create superuser'

    def handle(self, *args, **options):
        self.stdout.write('Setting up database...')
        
        # Run migrations with syncdb
        self.stdout.write('Running migrations...')
        try:
            call_command('migrate', '--run-syncdb', verbosity=2)
            self.stdout.write(self.style.SUCCESS('Migrations completed successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Migration failed: {e}'))
            # Try alternative approach
            try:
                self.stdout.write('Trying alternative migration approach...')
                call_command('migrate', verbosity=2)
                self.stdout.write(self.style.SUCCESS('Alternative migrations completed'))
            except Exception as e2:
                self.stdout.write(self.style.ERROR(f'Both migration approaches failed: {e2}'))
                return
        
        # Check if database tables exist
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user'")
            if not cursor.fetchone():
                self.stdout.write(self.style.ERROR('auth_user table not found after migration'))
                return
        
        # Create superuser if it doesn't exist
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created: username=admin, password=admin123'))
        else:
            self.stdout.write('Superuser already exists')
        
        # Verify database setup
        self.stdout.write('Verifying database setup...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM auth_user")
                user_count = cursor.fetchone()[0]
                self.stdout.write(f'Found {user_count} users in database')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Database verification failed: {e}'))
            return
        
        self.stdout.write(self.style.SUCCESS('Database setup completed successfully!'))
