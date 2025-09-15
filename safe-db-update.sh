#!/bin/bash
# SAKU Election System - Database-Safe Update Script

set -e

echo "🔄 Starting Database-Safe Update for SAKU Election System"

# Step 1: Create database backup
echo "💾 Creating database backup..."
gcloud sql backups create \
    --instance=your-db-instance \
    --description="Pre-update backup $(date)"

# Step 2: Run migrations in dry-run mode
echo "🧪 Testing migrations..."
python manage.py makemigrations --dry-run
python manage.py migrate --dry-run

# Step 3: Deploy new version
echo "📦 Deploying new version..."
gcloud run deploy saku-election-system \
    --source . \
    --platform managed \
    --region us-central1

# Step 4: Run migrations
echo "🗄️ Applying database migrations..."
gcloud run jobs create migration-job \
    --image gcr.io/your-project/saku-election-system \
    --region us-central1 \
    --command python \
    --args manage.py,migrate

gcloud run jobs execute migration-job --region us-central1

# Step 5: Verify deployment
echo "✅ Verifying deployment..."
SERVICE_URL=$(gcloud run services describe saku-election-system --region=us-central1 --format='value(status.url)')
if curl -f "$SERVICE_URL/" > /dev/null 2>&1; then
    echo "🎉 Update completed successfully!"
    echo "🌐 Your SAKU Election System is live at: $SERVICE_URL"
else
    echo "❌ Deployment verification failed!"
    echo "🔄 Consider rolling back..."
fi
