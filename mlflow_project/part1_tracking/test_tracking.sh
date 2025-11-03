#!/bin/bash

echo "=========================================="
echo "Part 1: Testing MLflow Tracking"
echo "=========================================="
echo ""

# Make sure MLflow server is running
echo "Checking if MLflow server is running..."
if ! curl -s http://localhost:5000 > /dev/null; then
    echo "❌ MLflow server is not running!"
    echo "   Start it with: mlflow server --host 0.0.0.0 --port 5000"
    exit 1
fi
echo "✓ MLflow server is running"
echo ""

# 1.1 & 1.2: First training run
echo "Step 1.1 & 1.2: First training run with default parameters"
echo "-----------------------------------------------------------"
python train_model.py --n-estimators 100 --max-depth 10
echo ""

# 1.3: Second run with different hyperparameters
echo "Step 1.3: Second run with modified hyperparameters"
echo "-----------------------------------------------------------"
python train_model.py --n-estimators 200 --max-depth 15
echo ""

# 1.4: Third run ensuring model is saved
echo "Step 1.4: Third run with different parameters"
echo "-----------------------------------------------------------"
python train_model.py --n-estimators 50 --max-depth 5 --min-samples-split 5
echo ""

echo "=========================================="
echo "All tracking tests completed!"
echo "=========================================="
echo ""
echo "✓ Check MLflow UI at: http://localhost:5000"
echo "✓ You should see 3 runs with different hyperparameters"
echo "✓ Each run should have:"
echo "   - Hyperparameters logged"
echo "   - Metrics (accuracy, f1, etc.)"
echo "   - Model artifacts saved"
echo ""

