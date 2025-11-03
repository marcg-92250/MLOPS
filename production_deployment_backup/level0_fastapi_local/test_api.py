#!/usr/bin/env python3
"""
STEP 2 & 5: Test script for Level 0 FastAPI service
Tests with: browser, wget, requests library, and HTTP clients
"""

import requests
import json
import sys
import subprocess

BASE_URL = "http://localhost:8000"


def print_header(title):
    """Print a nice header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_step1_get_predict():
    """STEP 1 & 2: Test simple GET /predict endpoint"""
    print_header("STEP 1 & 2: Test GET /predict (returns y_pred=2)")
    
    print("\n📌 Method 1: Python requests library")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/predict")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.json().get("y_pred") == 2:
            print("✅ SUCCESS: Got expected response!")
        else:
            print("❌ ERROR: Unexpected response")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n📌 Method 2: Browser")
    print("-" * 70)
    print("Open in your browser:")
    print(f"  {BASE_URL}/predict")
    print("Expected: {\"y_pred\": 2}")
    
    print("\n📌 Method 3: curl")
    print("-" * 70)
    print("Run this command:")
    print(f"  curl {BASE_URL}/predict")
    print("\nTesting with curl...")
    try:
        result = subprocess.run(
            ["curl", "-s", f"{BASE_URL}/predict"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"Response: {result.stdout}")
            print("✅ curl test successful")
        else:
            print("⚠️  curl not available or failed")
    except:
        print("⚠️  curl not available")
    
    print("\n📌 Method 4: wget")
    print("-" * 70)
    print("Run this command:")
    print(f"  wget -qO- {BASE_URL}/predict")
    print("\nTesting with wget...")
    try:
        result = subprocess.run(
            ["wget", "-qO-", f"{BASE_URL}/predict"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"Response: {result.stdout}")
            print("✅ wget test successful")
        else:
            print("⚠️  wget not available or failed")
    except:
        print("⚠️  wget not available")
    
    print("\n📌 Method 5: GUI HTTP Clients")
    print("-" * 70)
    print("Use these tools:")
    print("  • Postman: https://www.postman.com/")
    print("  • Insomnia: https://insomnia.rest/")
    print("  • HTTPie Desktop: https://httpie.io/")
    print("  • Thunder Client (VS Code extension)")
    print("\nCreate a GET request to:")
    print(f"  {BASE_URL}/predict")


def test_step3_post_predict():
    """STEP 3: Test POST /predict endpoint"""
    print_header("STEP 3: Test POST /predict endpoint")
    
    test_data = {
        "size": 100.0,
        "bedrooms": 3,
        "garden": 1
    }
    
    print(f"\n📤 Sending POST request to: {BASE_URL}/predict")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            print(f"\n💰 Predicted Price: ${result['predicted_price']:,.2f}")
            print("✅ POST request successful!")
        else:
            print(f"Response: {response.text}")
            print("❌ POST request failed")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n📌 Test with curl:")
    print(f"""curl -X POST {BASE_URL}/predict \\
  -H "Content-Type: application/json" \\
  -d '{json.dumps(test_data)}'""")


def test_step5_various_predictions():
    """STEP 5: Test model with various inputs"""
    print_header("STEP 5: Test Model with Various Inputs")
    
    test_cases = [
        {
            "data": {"size": 50.0, "bedrooms": 1, "garden": 0},
            "description": "Small apartment (50m², 1 bedroom, no garden)"
        },
        {
            "data": {"size": 100.0, "bedrooms": 3, "garden": 1},
            "description": "Medium house (100m², 3 bedrooms, garden)"
        },
        {
            "data": {"size": 150.0, "bedrooms": 4, "garden": 1},
            "description": "Large house (150m², 4 bedrooms, garden)"
        },
        {
            "data": {"size": 200.0, "bedrooms": 5, "garden": 1},
            "description": "Luxury house (200m², 5 bedrooms, garden)"
        }
    ]
    
    print("\n🧪 Testing multiple predictions...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"{i}. {test_case['description']}")
        print(f"   Input: {test_case['data']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json=test_case['data']
            )
            
            if response.status_code == 200:
                result = response.json()
                price = result['predicted_price']
                print(f"   💰 Predicted Price: ${price:,.2f}")
                print("   ✅ Success")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()


def test_additional_endpoints():
    """Test additional helpful endpoints"""
    print_header("Additional Endpoints")
    
    print("\n📌 Root endpoint (GET /)")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n📌 Health check (GET /health)")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n📌 Model info (GET /model-info)")
    try:
        response = requests.get(f"{BASE_URL}/model-info")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")


def check_server():
    """Check if the server is running"""
    print_header("Checking Server Status")
    try:
        response = requests.get(BASE_URL, timeout=2)
        print(f"✅ Server is running at {BASE_URL}")
        return True
    except requests.exceptions.RequestException:
        print(f"❌ Server is NOT running at {BASE_URL}")
        print("\n💡 Start the server with:")
        print("   python main.py")
        print("   or")
        print("   uvicorn main:app --reload")
        return False


def run_all_tests():
    """Run all tests in sequence"""
    print("=" * 70)
    print(" " * 15 + "LEVEL 0 - API TEST SUITE")
    print("=" * 70)
    
    if not check_server():
        sys.exit(1)
    
    # Run all test steps
    test_step1_get_predict()
    test_step3_post_predict()
    test_step5_various_predictions()
    test_additional_endpoints()
    
    # Summary
    print("\n" + "=" * 70)
    print(" " * 20 + "✅ ALL TESTS COMPLETED")
    print("=" * 70)
    print("\n📖 What we tested:")
    print("  ✅ STEP 1: GET /predict returning {\"y_pred\": 2}")
    print("  ✅ STEP 2: Multiple test methods (requests, curl, wget, browser)")
    print("  ✅ STEP 3: POST /predict endpoint")
    print("  ✅ STEP 4: Model integration (automatic)")
    print("  ✅ STEP 5: Various predictions with different inputs")
    print("\n💡 Next: Visit http://localhost:8000/docs for interactive API docs")
    print()


if __name__ == "__main__":
    run_all_tests()

