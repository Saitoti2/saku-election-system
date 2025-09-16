#!/bin/bash

echo "🚀 SAKU Election System - Render Deployment Script"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Project structure verified"

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found."
    exit 1
fi

echo "✅ Requirements file found"

# Check if Procfile exists
if [ ! -f "Procfile" ]; then
    echo "❌ Error: Procfile not found."
    exit 1
fi

echo "✅ Procfile found"

# Check if start.sh exists and is executable
if [ ! -f "start.sh" ]; then
    echo "❌ Error: start.sh not found."
    exit 1
fi

if [ ! -x "start.sh" ]; then
    echo "⚠️  Making start.sh executable..."
    chmod +x start.sh
fi

echo "✅ Start script ready"

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found."
    exit 1
fi

echo "✅ Frontend files found"

# Check if elections app exists
if [ ! -d "elections" ]; then
    echo "❌ Error: elections app not found."
    exit 1
fi

echo "✅ Elections app found"

# Check if core app exists
if [ ! -d "core" ]; then
    echo "❌ Error: core app not found."
    exit 1
fi

echo "✅ Core app found"

echo ""
echo "🎯 Deployment Checklist:"
echo "========================"
echo "✅ All required files present"
echo "✅ Project structure verified"
echo "✅ Scripts are executable"
echo ""
echo "📋 Next Steps for Render Deployment:"
echo "===================================="
echo "1. Push this code to GitHub:"
echo "   git add ."
echo "   git commit -m 'Ready for Render deployment'"
echo "   git push origin main"
echo ""
echo "2. Go to render.com and create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Use these settings:"
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: ./start.sh"
echo ""
echo "5. Create a PostgreSQL database on Render"
echo "6. Add DATABASE_URL environment variable"
echo "7. Add other environment variables as needed"
echo ""
echo "8. Deploy and test!"
echo ""
echo "🔗 Useful URLs after deployment:"
echo "================================"
echo "• Health Check: https://your-app.onrender.com/"
echo "• Admin Panel: https://your-app.onrender.com/admin/"
echo "• Login Page: https://your-app.onrender.com/login/"
echo "• Registration: https://your-app.onrender.com/register/"
echo ""
echo "🔑 Default Admin Login:"
echo "======================="
echo "Username: admin"
echo "Password: admin123"
echo ""
echo "📚 Documentation:"
echo "================="
echo "• README.md - Complete system documentation"
echo "• RENDER_DEPLOYMENT_GUIDE.md - Detailed deployment steps"
echo ""
echo "🎉 Your SAKU Election System is ready for deployment!"
echo "====================================================="
