#!/bin/bash

echo "🗳️ Starting SAKU Election System..."
echo "=================================="

# Check if we're in the right directory
if [ ! -d "saku-strategy" ]; then
    echo "❌ Error: saku-strategy directory not found"
    echo "Make sure you're in the project root directory"
    exit 1
fi

# Navigate to backend directory
cd saku-strategy/backend

echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo "🗄️ Running database migrations..."
python3 manage.py migrate

echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

echo "🚀 Starting Django backend server..."
python3 manage.py runserver 0.0.0.0:8001 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Navigate to frontend directory
cd ../frontend

echo "🌐 Starting frontend server..."
python3 serve.py &
FRONTEND_PID=$!

echo ""
echo "✅ SAKU Election System is now running!"
echo "=================================="
echo "🌐 Frontend (Student Portal): http://localhost:5173"
echo "🔧 Backend (Admin Dashboard): http://localhost:8001"
echo ""
echo "📱 Features Available:"
echo "   ✅ Student registration portal"
echo "   ✅ Admin dashboard"
echo "   ✅ Document upload system"
echo "   ✅ Mobile-responsive design"
echo ""
echo "🎯 For your presentation:"
echo "   1. Open http://localhost:5173 in your browser"
echo "   2. Demo the student portal features"
echo "   3. Show mobile responsiveness"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait