#!/bin/bash
#
# Quick deployment script for Level 0.5
# Deploy code to remote machine
#

set -e  # Exit on error

# Configuration
REMOTE_HOST="74.234.179.93"
REMOTE_USER="ubuntu"
REMOTE_DIR="/home/ubuntu/gma/deployment"
LOCAL_DIR="/home/gma/MLOPS/production_deployment"

echo "=========================================="
echo "   Remote Deployment Script"
echo "=========================================="
echo ""

# Check if local directory exists
if [ ! -d "$LOCAL_DIR" ]; then
    echo "❌ Error: Local directory not found: $LOCAL_DIR"
    exit 1
fi

echo "📦 Preparing deployment..."
echo "   From: $LOCAL_DIR"
echo "   To:   $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
echo ""

# Option 1: Using rsync (recommended)
echo "🚀 Deploying with rsync..."
rsync -avz --progress \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.git' \
    --exclude 'venv' \
    --exclude '.venv' \
    -e ssh \
    "$LOCAL_DIR/" \
    "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. SSH to remote machine:"
    echo "      ssh $REMOTE_USER@$REMOTE_HOST"
    echo ""
    echo "   2. Navigate to deployment folder:"
    echo "      cd $REMOTE_DIR/level0_local"
    echo ""
    echo "   3. Install dependencies:"
    echo "      pip install fastapi uvicorn joblib scikit-learn numpy"
    echo ""
    echo "   4. Start the service:"
    echo "      uvicorn main:app --host 0.0.0.0 --port 8001"
    echo ""
    echo "   5. Test from local machine:"
    echo "      curl http://$REMOTE_HOST:8001/predict"
    echo ""
else
    echo ""
    echo "❌ Deployment failed!"
    exit 1
fi

