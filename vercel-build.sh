#!/bin/bash
# Vercel build script for frontend only
# This script ensures Python is not installed

echo "🚀 Starting Vercel build for frontend..."

# Skip Python installation
echo "✅ Skipping Python dependencies (frontend only)"

# Run the API URL injection script
if [ -f inject-api-url.js ]; then
    echo "📝 Injecting API URL into HTML files..."
    node inject-api-url.js
    echo "✅ API URL injection complete"
else
    echo "⚠️  inject-api-url.js not found, skipping"
fi

echo "✨ Build complete!"

