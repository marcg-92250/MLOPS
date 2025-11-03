#!/usr/bin/env python3
"""
Test script for the FastAPI service
Tests with: requests library, wget simulation, and various HTTP methods
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"


def test_with_browser():
    """Step 2: Test with browser simulation (GET request)"""
    print("=" * 60)
    print("Test 1: Browser / GET Request")
    print("=" * 60)
    
    print(f"\n📍 URL: {BASE_URL}/predict")
    print("Method: GET")
    print("\nYou can test in browser at: http://localhost:8000/predict")
    print("Or use: curl http://localhost:8000/predict")
    
    try:
        response = requests.get(f"{BASE_URL}/predict")
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✓ GET request successful")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_with_requests():
    """Step 2: Test with Python requests library"""
    print("\n" + "=" * 60)
    print("Test 2: Python requests library")
    print("=" * 60)
    
    try:
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        response = requests.get(BASE_URL)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {json.dumps(response.json(), indent=2)}")
        
        print("\n✓ Requests library tests successful")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_post_request():
    """Step 3: Test POST request"""
    print("\n" + "=" * 60)
    print("Test 3: POST Request")
    print("=" * 60)
    
    # Test data
    house_data = {
        "size": 100.0,
        "bedrooms": 3,
        "garden": 1
    }
    
    print(f"\nSending POST request to: {BASE_URL}/predict")
    print(f"Data: {json.dumps(house_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=house_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print(f"\n💰 Predicted Price: ${result['predicted_price']:,.2f}")
            print("✓ POST request successful")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_model_prediction():
    """Step 4-5: Test model predictions with various inputs"""
    print("\n" + "=" * 60)
    print("Test 4: Model Predictions")
    print("=" * 60)
    
    test_cases = [
        {"size": 50.0, "bedrooms": 1, "garden": 0, "description": "Small apartment"},
        {"size": 100.0, "bedrooms": 3, "garden": 1, "description": "Medium house with garden"},
        {"size": 150.0, "bedrooms": 4, "garden": 1, "description": "Large house with garden"},
        {"size": 200.0, "bedrooms": 5, "garden": 1, "description": "Luxury villa"}
    ]
    
    print("\nTesting multiple predictions...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        description = test_case.pop("description")
        print(f"{i}. {description}")
        print(f"   Features: {test_case}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   💰 Predicted Price: ${result['predicted_price']:,.2f}")
            else:
                print(f"   Error: {response.status_code}")
                
        except Exception as e:
            print(f"   Error: {e}")
        
        print()


def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("=" * 60)
    print("Test 5: Batch Prediction")
    print("=" * 60)
    
    batch_data = {
        "houses": [
            {"size": 50.0, "bedrooms": 1, "garden": 0},
            {"size": 100.0, "bedrooms": 3, "garden": 1},
            {"size": 150.0, "bedrooms": 4, "garden": 1}
        ]
    }
    
    print(f"\nSending batch request for {len(batch_data['houses'])} houses...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict-batch",
            json=batch_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ Received {result['count']} predictions:")
            for i, price in enumerate(result['predictions'], 1):
                print(f"   House {i}: ${price:,.2f}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def test_model_info():
    """Test model info endpoint"""
    print("\n" + "=" * 60)
    print("Test 6: Model Information")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        
        if response.status_code == 200:
            info = response.json()
            print("\n📊 Model Information:")
            print(f"   Type: {info['model_type']}")
            print(f"   Features: {info['features']}")
            print(f"\n   Coefficients:")
            for feature, coef in info['coefficients'].items():
                print(f"     {feature}: {coef:.2f}")
            print(f"   Intercept: {info['intercept']:.2f}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"✗ Error: {e}")


def show_curl_examples():
    """Show curl command examples"""
    print("\n" + "=" * 60)
    print("Curl Command Examples")
    print("=" * 60)
    
    print("\n1. GET request:")
    print(f"   curl {BASE_URL}/predict")
    
    print("\n2. POST request:")
    print(f"""   curl -X POST {BASE_URL}/predict \\
        -H "Content-Type: application/json" \\
        -d '{{"size": 100, "bedrooms": 3, "garden": 1}}'""")
    
    print("\n3. Health check:")
    print(f"   curl {BASE_URL}/health")
    
    print("\n4. Model info:")
    print(f"   curl {BASE_URL}/model-info")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print(" " * 15 + "FastAPI Service Test Suite")
    print("=" * 70)
    
    try:
        # Check if service is running
        print("\n✓ Checking if service is running...")
        response = requests.get(BASE_URL, timeout=2)
        print(f"  Service is UP at {BASE_URL}")
    except requests.exceptions.RequestException:
        print(f"\n✗ Service is not running at {BASE_URL}")
        print("\nStart the service with:")
        print("  uvicorn main:app --reload")
        print("  or")
        print("  python main.py")
        sys.exit(1)
    
    # Run all tests
    test_with_browser()
    test_with_requests()
    test_post_request()
    test_model_prediction()
    test_batch_prediction()
    test_model_info()
    show_curl_examples()
    
    print("\n" + "=" * 70)
    print("✓ All tests completed!")
    print("=" * 70)
    print("\n💡 Tip: Visit http://localhost:8000/docs for interactive API docs")
    print()


if __name__ == "__main__":
    run_all_tests()

