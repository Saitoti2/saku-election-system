#!/bin/bash
# Script to push commits to GitHub
# This will help you push the latest commits

echo "🚀 Preparing to push commits to GitHub..."
echo ""

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: Not in the project root directory"
    exit 1
fi

# Show commits to be pushed
echo "📦 Commits ready to push:"
git log --oneline origin/main..HEAD
echo ""

# Try different push methods
echo "Attempting to push..."

# Method 1: Try with GitHub CLI
if command -v gh &> /dev/null; then
    echo "Trying GitHub CLI..."
    gh auth refresh -s repo 2>&1
    git push origin main 2>&1 && echo "✅ Successfully pushed!" && exit 0
fi

# Method 2: Try regular push
echo "Trying regular git push..."
git push origin main 2>&1

echo ""
echo "If push failed, please:"
echo "1. Open GitHub Desktop and click 'Push origin'"
echo "2. Or use VS Code Source Control panel"
echo "3. Or authenticate with: gh auth login"

