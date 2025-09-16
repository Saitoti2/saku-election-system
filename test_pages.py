"""
Test pages for verifying deployment
"""
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth import get_user_model

def test_database(request):
    """Test database connectivity and show status"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Check auth_user table
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            user_count = cursor.fetchone()[0]
            
        html = f"""
        <html>
        <head><title>Database Test - SAKU Election System</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🗄️ Database Test Results</h1>
            <h2>✅ Database Connection: SUCCESS</h2>
            <p><strong>Tables Found:</strong> {len(tables)}</p>
            <ul>
                {''.join([f'<li>{table}</li>' for table in tables])}
            </ul>
            <p><strong>Users in Database:</strong> {user_count}</p>
            <hr>
            <h2>🔗 Quick Links:</h2>
            <ul>
                <li><a href="/admin/">Admin Panel</a></li>
                <li><a href="/login/">Login Page</a></li>
                <li><a href="/admin-dashboard/">Admin Dashboard</a></li>
                <li><a href="/register/">Registration</a></li>
                <li><a href="/api/">API Root</a></li>
            </ul>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Exception as e:
        html = f"""
        <html>
        <head><title>Database Test - SAKU Election System</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>❌ Database Test Failed</h1>
            <p><strong>Error:</strong> {str(e)}</p>
        </body>
        </html>
        """
        return HttpResponse(html, status=500)

def test_auth(request):
    """Test authentication system"""
    try:
        User = get_user_model()
        users = User.objects.all()
        
        html = f"""
        <html>
        <head><title>Auth Test - SAKU Election System</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>🔐 Authentication Test</h1>
            <h2>✅ Authentication System: WORKING</h2>
            <p><strong>Total Users:</strong> {users.count()}</p>
            <ul>
                {''.join([f'<li>{user.username} ({user.email}) - {"Superuser" if user.is_superuser else "Regular"}</li>' for user in users])}
            </ul>
            <hr>
            <p><a href="/admin/">Go to Admin Panel</a></p>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Exception as e:
        html = f"""
        <html>
        <head><title>Auth Test - SAKU Election System</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px;">
            <h1>❌ Authentication Test Failed</h1>
            <p><strong>Error:</strong> {str(e)}</p>
        </body>
        </html>
        """
        return HttpResponse(html, status=500)
