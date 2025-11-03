#!/usr/bin/env python3
"""
Test script for Level 1 - Docker deployment
Tests the containerized FastAPI service
"""

import requests
import time
import sys

BASE_URL = "http://localhost:8000"


def print_header(title):
    """Print a nice header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def wait_for_service(timeout=30):
    """Wait for the service to be ready"""
    print_header("Waiting for Service to Start")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(BASE_URL, timeout=2)
            if response.status_code == 200:
                print(f"✅ Service is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print("⏳ Waiting for service...", end="\r")
        time.sleep(1)
    
    print(f"\n❌ Service did not start within {timeout} seconds")
    return False


def test_root():
    """Test root endpoint"""
    print_header("Test 1: Root Endpoint (GET /)")
    
    try:
        response = requests.get(BASE_URL)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Message: {data.get('message')}")
            print(f"Version: {data.get('version')}")
            print(f"Model loaded: {data.get('model_loaded')}")
            print("✅ Root endpoint working")
            return True
        else:
            print("❌ Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_health():
    """Test health endpoint"""
    print_header("Test 2: Health Check (GET /health)")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Health: {data}")
            print("✅ Health endpoint working")
            return True
        else:
            print("❌ Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_get_predict():
    """Test GET /predict (preamble)"""
    print_header("Test 3: GET /predict (Preamble)")
    
    try:
        response = requests.get(f"{BASE_URL}/predict")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("y_pred") == 2:
                print("✅ GET /predict working correctly")
                return True
            else:
                print("⚠️  Unexpected response value")
                return False
        else:
            print("❌ Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_post_predict():
    """Test POST /predict with model"""
    print_header("Test 4: POST /predict (Model Prediction)")
    
    test_data = {
        "size": 100.0,
        "bedrooms": 3,
        "garden": 1
    }
    
    print(f"Input: {test_data}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Predicted price: ${data['predicted_price']:,.2f}")
            print(f"Input features: {data['input_features']}")
            print("✅ POST /predict working correctly")
            return True
        else:
            print(f"Response: {response.text}")
            print("❌ Unexpected status code")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_multiple_predictions():
    """Test with various house configurations"""
    print_header("Test 5: Multiple Predictions")
    
    test_cases = [
        {"size": 50, "bedrooms": 1, "garden": 0, "desc": "Small apt"},
        {"size": 100, "bedrooms": 3, "garden": 1, "desc": "Medium house"},
        {"size": 150, "bedrooms": 4, "garden": 1, "desc": "Large house"},
        {"size": 200, "bedrooms": 5, "garden": 1, "desc": "Luxury house"},
    ]
    
    success = True
    for i, case in enumerate(test_cases, 1):
        desc = case.pop("desc")
        print(f"\n{i}. {desc}: {case}")
        
        try:
            response = requests.post(f"{BASE_URL}/predict", json=case)
            
            if response.status_code == 200:
                price = response.json()["predicted_price"]
                print(f"   💰 Predicted: ${price:,.2f}")
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                success = False
        except Exception as e:
            print(f"   ❌ Error: {e}")
            success = False
    
    return success


def test_model_info():
    """Test model info endpoint"""
    print_header("Test 6: Model Info (GET /model-info)")
    
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Model type: {data.get('model_type')}")
            print(f"Features: {data.get('features')}")
            print(f"Coefficients: {data.get('coefficients')}")
            print(f"Intercept: {data.get('intercept')}")
            print("✅ Model info endpoint working")
            return True
        else:
            print("⚠️  Model info not available")
            return False
    except Exception as e:
        print(f"⚠️  Model info error: {e}")
        return False


def test_docs_available():
    """Check if docs are accessible"""
    print_header("Test 7: API Documentation")
    
    try:
        response = requests.get(f"{BASE_URL}/docs")
        
        if response.status_code == 200:
            print(f"📖 Interactive docs available at: {BASE_URL}/docs")
            print("✅ Documentation endpoint working")
            return True
        else:
            print("⚠️  Docs not available")
            return False
    except Exception as e:
        print(f"⚠️  Docs error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("  🐳 DOCKER DEPLOYMENT TEST SUITE")
    print("="*70)
    print(f"\nTesting: {BASE_URL}")
    
    # Wait for service
    if not wait_for_service():
        print("\n❌ Service not available. Make sure Docker container is running:")
        print("   docker run -d -p 8000:8000 --name house-api house-price-api:v1")
        sys.exit(1)
    
    # Run all tests
    results = []
    results.append(("Root Endpoint", test_root()))
    results.append(("Health Check", test_health()))
    results.append(("GET /predict", test_get_predict()))
    results.append(("POST /predict", test_post_predict()))
    results.append(("Multiple Predictions", test_multiple_predictions()))
    results.append(("Model Info", test_model_info()))
    results.append(("API Docs", test_docs_available()))
    
    # Summary
    print("\n" + "="*70)
    print("  📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {test_name}")
    
    print("\n" + "="*70)
    print(f"  Results: {passed}/{total} tests passed")
    print("="*70)
    
    if passed == total:
        print("\n🎉 All tests passed! Your Docker container is working perfectly!")
        print(f"\n📖 Visit {BASE_URL}/docs for interactive API documentation")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the output above.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

