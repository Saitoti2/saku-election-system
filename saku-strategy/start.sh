#!/bin/bash
set -e

echo "🚀 Starting SAKU Strategy App..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Please run this script from the saku-strategy root directory"
    exit 1
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $1 is already in use"
        return 1
    else
        return 0
    fi
}

# Check ports
if ! check_port 8000; then
    echo "Backend port 8000 is in use. Please stop the existing service or use a different port."
    exit 1
fi

if ! check_port 5173; then
    echo "Frontend port 5173 is in use. Please stop the existing service or use a different port."
    exit 1
fi

# Start backend
echo "📦 Starting backend server..."
cd backend
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Seed sample data if no data exists
if [ $(python manage.py shell -c "from elections.models import Delegate; print(Delegate.objects.count())") -eq 0 ]; then
    echo "🌱 Seeding sample data..."
    PYTHONPATH=. python scripts/seed_sample_data.py
fi

# Start backend server
echo "🚀 Starting Django server on http://localhost:8000"
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Test backend
if curl -s http://localhost:8000/api/departments/ > /dev/null; then
    echo "✅ Backend is running successfully"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start frontend (if Node.js is available)
cd ../frontend
if command -v npm &> /dev/null; then
    echo "📦 Starting frontend server..."
    if [ ! -d "node_modules" ]; then
        echo "Installing frontend dependencies..."
        npm install
    fi
    
    echo "🚀 Starting Vite server on http://localhost:5173"
    npm run dev &
    FRONTEND_PID=$!
    
    echo ""
    echo "🎉 SAKU Strategy App is running!"
    echo ""
    echo "📊 Access points:"
    echo "   Frontend Dashboard: http://localhost:5173"
    echo "   Backend API: http://localhost:8000"
    echo "   Admin Interface: http://localhost:8000/admin (admin/admin123)"
    echo ""
    echo "🔧 API Endpoints:"
    echo "   GET /api/departments/ - List departments"
    echo "   GET /api/delegates/metrics/ - Coverage metrics"
    echo "   GET /api/delegates/risks/ - Risk assessment"
    echo "   POST /api/delegates/simulate/ - What-if simulation"
    echo ""
    echo "Press Ctrl+C to stop all services"
    
    # Wait for user interrupt
    trap "echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit 0" INT
    wait
else
    echo "⚠️  Node.js not found. Frontend will not start."
    echo "   Install Node.js to run the frontend, or use Docker: docker compose up --build"
    echo ""
    echo "🎉 Backend is running!"
    echo "   Backend API: http://localhost:8000"
    echo "   Admin Interface: http://localhost:8000/admin (admin/admin123)"
    echo ""
    echo "Press Ctrl+C to stop the backend"
    
    # Wait for user interrupt
    trap "echo '🛑 Stopping backend...'; kill $BACKEND_PID 2>/dev/null || true; exit 0" INT
    wait
fi

