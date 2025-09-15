#!/bin/bash
# SAKU Election System - Emergency Rollback Script

set -e

SERVICE_NAME="saku-election-system"
REGION="us-central1"

echo "🚨 Emergency Rollback for SAKU Election System"

# Method 1: Rollback to previous revision
echo "🔄 Rolling back to previous revision..."
PREVIOUS_REVISION=$(gcloud run revisions list \
    --service=$SERVICE_NAME \
    --region=$REGION \
    --limit=2 \
    --format='value(metadata.name)' | tail -1)

echo "📦 Rolling back to revision: $PREVIOUS_REVISION"

gcloud run services update-traffic $SERVICE_NAME \
    --region $REGION \
    --to-revisions $PREVIOUS_REVISION=100

echo "✅ Rollback completed!"
echo "🌐 Service is now running the previous version"

# Method 2: Quick redeploy from last known good commit
echo ""
echo "🔄 Alternative: Redeploy from last known good commit..."
echo "Run this command:"
echo "git checkout HEAD~1"
echo "gcloud run deploy $SERVICE_NAME --source . --region $REGION"
echo "git checkout main"
