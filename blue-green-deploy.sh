#!/bin/bash
# SAKU Election System - Blue-Green Deployment Script

set -e

PROJECT_ID="your-project-id"
SERVICE_NAME="saku-election-system"
REGION="us-central1"
NEW_VERSION="v$(date +%Y%m%d-%H%M%S)"

echo "🚀 Starting Blue-Green Deployment for SAKU Election System"

# Step 1: Deploy new version with traffic split
echo "📦 Deploying new version: $NEW_VERSION"
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --tag $NEW_VERSION \
    --no-traffic \
    --memory 512Mi \
    --cpu 1

# Step 2: Test new version
echo "🧪 Testing new version..."
NEW_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
NEW_URL="${NEW_URL%/*}/$NEW_VERSION"

# Health check
echo "🔍 Running health check..."
if curl -f "$NEW_URL/" > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "❌ Health check failed! Rolling back..."
    exit 1
fi

# Step 3: Gradually shift traffic (optional)
echo "🔄 Shifting 10% traffic to new version..."
gcloud run services update-traffic $SERVICE_NAME \
    --region $REGION \
    --to-tags $NEW_VERSION=10

sleep 30

echo "🔄 Shifting 50% traffic to new version..."
gcloud run services update-traffic $SERVICE_NAME \
    --region $REGION \
    --to-tags $NEW_VERSION=50

sleep 30

# Step 4: Full traffic shift
echo "🎯 Shifting 100% traffic to new version..."
gcloud run services update-traffic $SERVICE_NAME \
    --region $REGION \
    --to-tags $NEW_VERSION=100

echo "✅ Blue-Green deployment completed successfully!"
echo "🌐 Your SAKU Election System is live at: $(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')"
