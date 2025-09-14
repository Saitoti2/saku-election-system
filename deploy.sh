#!/bin/bash

# SAKU Election System - Railway Deployment Script

echo "🚀 Preparing SAKU Election System for Railway deployment..."

# Check if we're in the right directory
if [ ! -f "Procfile" ]; then
    echo "❌ Error: Procfile not found. Make sure you're in the project root directory."
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - SAKU Election System"
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📥 Installing Railway CLI..."
    curl -fsSL https://railway.app/install.sh | sh
fi

echo "✅ All checks passed!"
echo ""
echo "🎯 Next steps:"
echo "1. Go to https://railway.app"
echo "2. Sign up with GitHub"
echo "3. Click 'New Project' → 'Deploy from GitHub repo'"
echo "4. Select your repository"
echo "5. Add environment variables from RAILWAY_CONFIG.md"
echo "6. Deploy!"
echo ""
echo "🌐 Your app will be live at: https://[random-name].railway.app"
echo ""
echo "📋 Required Environment Variables:"
echo "   SECRET_KEY=your-production-secret-key"
echo "   DEBUG=False"
echo "   ALLOWED_HOSTS=*.railway.app"
echo "   ADMIN_PHONE_NUMBER=+254769582779"
