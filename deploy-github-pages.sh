#!/bin/bash

# SAKU Election System - GitHub Pages Deployment Script

echo "🚀 Deploying SAKU Election System to GitHub Pages..."

# Check if we're in the right directory
if [ ! -f "index.html" ]; then
    echo "❌ Error: index.html not found. Make sure you're in the project root directory."
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - SAKU Election System"
fi

# Add all files to git
echo "📝 Adding files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Deploy SAKU Election System to GitHub Pages - $(date)"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Deployment complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Go to your GitHub repository settings"
echo "2. Scroll down to 'Pages' section"
echo "3. Select 'GitHub Actions' as source"
echo "4. Your site will be available at: https://YOUR_USERNAME.github.io/YOUR_REPO_NAME"
echo ""
echo "🔄 Auto-deployment is enabled - every push to main branch will update your live site!"
echo ""
echo "📊 Your SAKU Election System features:"
echo "   ✅ Student registration portal"
echo "   ✅ Admin dashboard"
echo "   ✅ Document verification"
echo "   ✅ WhatsApp notifications"
echo "   ✅ Mobile-responsive design"
echo "   ✅ Automatic GitHub Pages deployment"
