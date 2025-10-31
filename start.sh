#!/bin/bash

echo "🗳️ Starting SAKU Election System..."
echo "=================================="

# Check if we're in the right directory
if [ ! -d "saku-strategy" ]; then
    echo "❌ Error: saku-strategy directory not found"
    echo "Make sure you're in the project root directory"
    exit 1
fi

PROJECT_ROOT="$(pwd)"
VENV_PATH="$PROJECT_ROOT/venv"

# Ensure a local virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "🧪 Creating local virtual environment..."
    python3 -m venv "$VENV_PATH" || {
        echo "❌ Failed to create virtual environment"
        exit 1
    }
fi

# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"

PYTHON="$(command -v python)"
PIP="$(command -v pip)"

echo "🐍 Using Python: $PYTHON"
echo "📦 Using Pip: $PIP"

# Navigate to backend directory
cd saku-strategy/backend

echo "📦 Installing backend dependencies..."
"$PIP" install --upgrade pip >/dev/null 2>&1
"$PIP" install -r requirements.txt

echo "🗄️ Running database migrations..."
"$PYTHON" manage.py migrate

echo "📁 Collecting static files..."
"$PYTHON" manage.py collectstatic --noinput

echo "🚀 Starting Django backend server..."
"$PYTHON" manage.py runserver 0.0.0.0:8001 &
DJANGO_PID=$!

# Wait a moment for Django to start
sleep 3

# Navigate to frontend directory
cd ../frontend

echo "🌐 Starting frontend server..."
"$PYTHON" serve.py &
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