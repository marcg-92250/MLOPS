#!/usr/bin/env python3
"""
Automated testing script for the model service
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    print("✓ Health check passed")
    print(f"  Response: {response.json()}")
    return response.json()


def test_update_model(model_name="wine_classification_model", version=None):
    """Test model update endpoint"""
    print(f"\nTesting /update-model endpoint...")
    print(f"  Model: {model_name}, Version: {version or 'latest'}")
    
    data = {"model_name": model_name}
    if version:
        data["version"] = version
    
    response = requests.post(
        f"{BASE_URL}/update-model",
        json=data
    )
    
    if response.status_code != 200:
        print(f"✗ Model update failed: {response.status_code}")
        print(f"  Error: {response.json()}")
        return False
    
    print("✓ Model updated successfully")
    print(f"  Response: {json.dumps(response.json(), indent=2)}")
    return True


def test_model_info():
    """Test model info endpoint"""
    print("\nTesting /model-info endpoint...")
    response = requests.get(f"{BASE_URL}/model-info")
    
    if response.status_code == 200:
        print("✓ Model info retrieved")
        print(f"  Response: {json.dumps(response.json(), indent=2)}")
        return response.json()
    else:
        print(f"✗ Failed to get model info: {response.status_code}")
        return None


def test_predict():
    """Test prediction endpoint"""
    print("\nTesting /predict endpoint...")
    
    # Wine dataset has 13 features
    test_data = {
        "features": [
            [14.23, 1.71, 2.43, 15.6, 127.0, 2.8, 3.06, 0.28, 2.29, 5.64, 1.04, 3.92, 1065.0],
            [13.2, 1.78, 2.14, 11.2, 100.0, 2.65, 2.76, 0.26, 1.28, 4.38, 1.05, 3.4, 1050.0]
        ]
    }
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=test_data
    )
    
    if response.status_code == 200:
        print("✓ Prediction successful")
        result = response.json()
        print(f"  Predictions: {result['predictions']}")
        print(f"  Model: {result['model_name']} v{result['model_version']}")
        return result
    else:
        print(f"✗ Prediction failed: {response.status_code}")
        print(f"  Error: {response.json()}")
        return None


def test_model_update_workflow():
    """Test complete model update workflow"""
    print("\n" + "="*60)
    print("Testing Model Update Workflow")
    print("="*60)
    
    # First prediction
    print("\n1. Making prediction with initial model...")
    result1 = test_predict()
    if not result1:
        print("  Skipping (no model loaded)")
    
    # Update model (could be a different version)
    print("\n2. Updating model...")
    test_update_model("wine_classification_model")
    
    # Second prediction
    print("\n3. Making prediction with updated model...")
    result2 = test_predict()
    
    if result1 and result2:
        print("\n4. Comparing results...")
        print(f"  First predictions:  {result1['predictions']}")
        print(f"  Second predictions: {result2['predictions']}")
        
        if result1['predictions'] == result2['predictions']:
            print("  ✓ Predictions are consistent (same model version)")
        else:
            print("  ℹ Predictions differ (possibly different model version)")


def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("MLflow Model Service - Automated Tests")
    print("="*60)
    
    try:
        # Check if service is running
        print("\nChecking if service is running...")
        response = requests.get(BASE_URL, timeout=2)
        print("✓ Service is running")
    except requests.exceptions.RequestException:
        print("✗ Service is not running!")
        print("  Start with: uvicorn model_service:app --reload")
        sys.exit(1)
    
    # Run tests
    test_health()
    
    # Try to update model first
    if test_update_model("wine_classification_model"):
        test_model_info()
        test_predict()
        test_model_update_workflow()
    else:
        print("\n⚠ Could not load model from MLflow")
        print("  Make sure you've run Part 1 (train_model.py) first")
        print("  And that MLflow server is running")
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()

