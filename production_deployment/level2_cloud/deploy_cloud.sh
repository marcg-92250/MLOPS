#!/bin/bash
#
# Automated deployment script for Level 2 - Cloud VM
# Deploys Docker container to remote VM
#

set -e  # Exit on error

# Configuration
VM_HOST="74.234.179.93"
VM_USER="ubuntu"
VM_DIR="/home/ubuntu/gma"
LOCAL_DIR="/home/gma/MLOPS/production_deployment/level1_docker"
VM_PORT=8001  # Change this to your assigned port

echo "=========================================="
echo "   Cloud VM Deployment Script"
echo "=========================================="
echo ""
echo "VM: $VM_USER@$VM_HOST"
echo "Directory: $VM_DIR"
echo "Port: $VM_PORT"
echo ""

# Check if local directory exists
if [ ! -d "$LOCAL_DIR" ]; then
    echo "❌ Error: Local directory not found: $LOCAL_DIR"
    exit 1
fi

# Step 1: Transfer files to VM
echo "📦 Step 1: Transferring files to VM..."
echo ""

rsync -avz --progress \
    -e ssh \
    "$LOCAL_DIR/Dockerfile" \
    "$LOCAL_DIR/main.py" \
    "$LOCAL_DIR/requirements.txt" \
    "$LOCAL_DIR/models/" \
    "$VM_USER@$VM_HOST:$VM_DIR/"

if [ $? -ne 0 ]; then
    echo "❌ File transfer failed"
    exit 1
fi

echo ""
echo "✅ Files transferred successfully"
echo ""

# Step 2: Build and run on VM
echo "🐳 Step 2: Building and running Docker container on VM..."
echo ""

ssh "$VM_USER@$VM_HOST" << EOF
    set -e
    
    echo "Navigating to deployment directory..."
    cd $VM_DIR
    
    echo "Stopping old container if exists..."
    docker stop house-api 2>/dev/null || true
    docker rm house-api 2>/dev/null || true
    
    echo "Building Docker image..."
    docker build -t house-price-api:v1 .
    
    echo "Running container on port $VM_PORT..."
    docker run -d -p $VM_PORT:8000 --name house-api house-price-api:v1
    
    echo ""
    echo "✅ Container deployed successfully!"
    echo ""
    
    echo "Container status:"
    docker ps | grep house-api || echo "Container not found in ps"
    
    echo ""
    echo "Container logs:"
    docker logs house-api
EOF

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "   ✅ DEPLOYMENT SUCCESSFUL"
echo "=========================================="
echo ""
echo "🌐 Your service is live at:"
echo "   http://$VM_HOST:$VM_PORT/predict"
echo ""
echo "📖 Interactive docs:"
echo "   http://$VM_HOST:$VM_PORT/docs"
echo ""
echo "🧪 Test with:"
echo "   curl http://$VM_HOST:$VM_PORT/predict"
echo ""
echo "🔍 View logs:"
echo "   ssh $VM_USER@$VM_HOST"
echo "   docker logs -f house-api"
echo ""
echo "📨 Share with friends:"
echo "   http://$VM_HOST:$VM_PORT/docs"
echo ""

