#!/bin/bash

echo "=========================================="
echo "MLflow Installation Script"
echo "=========================================="
echo ""

# Method 1: Local installation
echo "Method 1: Local Installation"
echo "----------------------------"
echo "Installing MLflow and dependencies..."

pip install mlflow scikit-learn pandas numpy -q

if [ $? -eq 0 ]; then
    echo "✓ MLflow installed successfully!"
    echo ""
    echo "To start MLflow server:"
    echo "  mlflow server --host 0.0.0.0 --port 5000"
    echo ""
    echo "Access UI at: http://localhost:5000"
else
    echo "✗ Installation failed"
    exit 1
fi

echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="

