#!/usr/bin/env python3
"""
Test script for remote deployment
Tests the API on the remote machine
"""

import requests
import sys

# Configuration
REMOTE_HOST = "74.234.179.93"
REMOTE_PORT = 8001  # Change this to your assigned port
BASE_URL = f"http://{REMOTE_HOST}:{REMOTE_PORT}"


def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_connection():
    """Test if we can reach the remote server"""
    print_header("Testing Connection")
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Connection successful!")
        print(f"   Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n💡 Make sure:")
        print(f"   1. Service is running on remote machine")
        print(f"   2. Using correct port: {REMOTE_PORT}")
        print(f"   3. Service bound to 0.0.0.0 (not 127.0.0.1)")
        return False


def test_get_predict():
    """Test GET /predict endpoint"""
    print_header("Testing GET /predict")
    
    url = f"{BASE_URL}/predict"
    print(f"📍 URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.json().get("y_pred") == 2:
            print("✅ GET /predict working correctly!")
            return True
        else:
            print("⚠️  Unexpected response")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_post_predict():
    """Test POST /predict endpoint"""
    print_header("Testing POST /predict")
    
    url = f"{BASE_URL}/predict"
    data = {
        "size": 100,
        "bedrooms": 3,
        "garden": 1
    }
    
    print(f"📍 URL: {url}")
    print(f"📤 Data: {data}")
    
    try:
        response = requests.post(url, json=data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ POST /predict working correctly!")
            return True
        else:
            print("⚠️  POST might not be implemented yet")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_multiple_predictions():
    """Test with various inputs"""
    print_header("Testing Multiple Predictions")
    
    test_cases = [
        {"size": 50, "bedrooms": 1, "garden": 0},
        {"size": 100, "bedrooms": 3, "garden": 1},
        {"size": 150, "bedrooms": 4, "garden": 1},
    ]
    
    url = f"{BASE_URL}/predict"
    
    for i, data in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {data}")
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                result = response.json()
                if 'predicted_price' in result:
                    print(f"   💰 Predicted: ${result['predicted_price']:,.2f}")
                else:
                    print(f"   Response: {result}")
                print(f"   ✅ Success")
            else:
                print(f"   ⚠️  Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def share_with_colleague():
    """Instructions for colleagues"""
    print_header("Share with Colleague")
    
    print(f"""
📨 Share this information with a colleague:

🌐 API Endpoint:
   {BASE_URL}/predict

🧪 Test Commands:

1. Browser:
   {BASE_URL}/predict

2. curl (GET):
   curl {BASE_URL}/predict

3. curl (POST):
   curl -X POST {BASE_URL}/predict \\
     -H "Content-Type: application/json" \\
     -d '{{"size": 100, "bedrooms": 3, "garden": 1}}'

4. Python:
   import requests
   response = requests.get("{BASE_URL}/predict")
   print(response.json())

📖 Interactive Docs:
   {BASE_URL}/docs

Ask your colleague to run these tests and confirm they can access your service!
""")


def main():
    print("\n" + "="*70)
    print("  🌐 REMOTE DEPLOYMENT TEST SUITE")
    print("="*70)
    print(f"\nTesting: {BASE_URL}")
    print(f"Time: {requests.utils.default_headers()}")
    
    # Run tests
    if not test_connection():
        sys.exit(1)
    
    test_get_predict()
    test_post_predict()
    test_multiple_predictions()
    share_with_colleague()
    
    # Summary
    print("\n" + "="*70)
    print("  ✅ TESTING COMPLETE")
    print("="*70)
    print(f"\n💡 Your service is live at: {BASE_URL}")
    print("   Share this URL with colleagues to test!\n")


if __name__ == "__main__":
    # Allow custom port from command line
    if len(sys.argv) > 1:
        REMOTE_PORT = int(sys.argv[1])
        BASE_URL = f"http://{REMOTE_HOST}:{REMOTE_PORT}"
        print(f"Using custom port: {REMOTE_PORT}")
    
    main()

