#!/bin/bash

# Level 3: Cloud Deployment Script
# Deploy Docker container to remote VM

set -e  # Exit on error

# Configuration
REMOTE_USER="ubuntu"
REMOTE_HOST="YOUR_VM_IP"  # Replace with actual IP
REMOTE_PORT="22"
LOCAL_IMAGE="house-price-api:latest"
REMOTE_PATH="/home/ubuntu/YOUR_INITIALS"  # Replace YOUR_INITIALS

echo "=========================================="
echo "Cloud Deployment Script"
echo "=========================================="
echo ""

# Step 1: Build Docker image locally
echo "Step 1: Building Docker image..."
cd ../level2_docker
docker build -t $LOCAL_IMAGE .
echo "✓ Image built"

# Step 2: Save image to tar
echo ""
echo "Step 2: Saving image to tar file..."
docker save -o house-price-api.tar $LOCAL_IMAGE
echo "✓ Image saved to tar"

# Step 3: Create remote directory
echo ""
echo "Step 3: Creating remote directory..."
ssh -p $REMOTE_PORT $REMOTE_USER@$REMOTE_HOST "mkdir -p $REMOTE_PATH"
echo "✓ Directory created"

# Step 4: Copy image to VM
echo ""
echo "Step 4: Copying image to VM..."
scp -P $REMOTE_PORT house-price-api.tar $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/
echo "✓ Image copied"

# Step 5: Load and run on VM
echo ""
echo "Step 5: Loading and running on VM..."
ssh -p $REMOTE_PORT $REMOTE_USER@$REMOTE_HOST << EOF
    cd $REMOTE_PATH
    docker load -i house-price-api.tar
    docker stop house-api 2>/dev/null || true
    docker rm house-api 2>/dev/null || true
    docker run -d -p 8000:8000 --name house-api --restart unless-stopped $LOCAL_IMAGE
    echo "✓ Container started"
    docker ps | grep house-api
EOF

# Cleanup
rm house-price-api.tar

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "Your API is now running at:"
echo "  http://$REMOTE_HOST:8000"
echo ""
echo "Test with:"
echo "  curl http://$REMOTE_HOST:8000/health"
echo ""

