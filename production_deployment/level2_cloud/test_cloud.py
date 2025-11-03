#!/usr/bin/env python3
"""
Test script for Level 2 - Cloud VM deployment
Tests the Docker container running on cloud VM
"""

import requests
import sys
import time

# Configuration
VM_HOST = "74.234.179.93"
VM_PORT = 8001  # Change to your assigned port
BASE_URL = f"http://{VM_HOST}:{VM_PORT}"


def print_header(title):
    """Print a nice header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_connection():
    """Test if we can reach the VM service"""
    print_header("Testing Connection to Cloud VM")
    
    print(f"Target: {BASE_URL}")
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        print(f"✅ Connection successful!")
        print(f"   Status: {response.status_code}")
        return True
    except requests.exceptions.Timeout:
        print(f"❌ Connection timeout")
        print(f"   The service might not be running or port {VM_PORT} is blocked")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Check if container is running on VM:")
        print(f"      ssh ubuntu@{VM_HOST}")
        print(f"      docker ps")
        print(f"   2. Check if port {VM_PORT} is correct")
        print(f"   3. Check if firewall allows port {VM_PORT}")
        return False


def test_get_predict():
    """Test GET /predict endpoint"""
    print_header("Testing GET /predict")
    
    url = f"{BASE_URL}/predict"
    print(f"📍 URL: {url}")
    
    try:
        response = requests.get(url, timeout=5)
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
        response = requests.post(url, json=data, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result}")
            if 'predicted_price' in result:
                print(f"💰 Predicted Price: ${result['predicted_price']:,.2f}")
            print("✅ POST /predict working correctly!")
            return True
        else:
            print(f"Response: {response.text}")
            print("❌ POST request failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_health():
    """Test health endpoint"""
    print_header("Testing Health Endpoint")
    
    url = f"{BASE_URL}/health"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"Health: {response.json()}")
            print("✅ Health check passed")
            return True
        else:
            print("⚠️  Health check failed")
            return False
    except Exception as e:
        print(f"⚠️  Health endpoint not available: {e}")
        return False


def test_multiple_predictions():
    """Test with various inputs"""
    print_header("Testing Multiple Predictions")
    
    test_cases = [
        {"size": 50, "bedrooms": 1, "garden": 0, "desc": "Small apt"},
        {"size": 100, "bedrooms": 3, "garden": 1, "desc": "Medium house"},
        {"size": 150, "bedrooms": 4, "garden": 1, "desc": "Large house"},
        {"size": 200, "bedrooms": 5, "garden": 1, "desc": "Luxury house"},
    ]
    
    url = f"{BASE_URL}/predict"
    success_count = 0
    
    for i, case in enumerate(test_cases, 1):
        desc = case.pop("desc")
        print(f"\n{i}. {desc}: {case}")
        
        try:
            response = requests.post(url, json=case, timeout=5)
            if response.status_code == 200:
                result = response.json()
                if 'predicted_price' in result:
                    price = result['predicted_price']
                    print(f"   💰 Price: ${price:,.2f}")
                    success_count += 1
                    print(f"   ✅ Success")
                else:
                    print(f"   Response: {result}")
            else:
                print(f"   ❌ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return success_count == len(test_cases)


def share_info():
    """Display sharing information"""
    print_header("Share with Colleagues")
    
    print(f"""
🌐 Your service is live on the cloud!

📍 Service URL:
   {BASE_URL}

🧪 Test endpoints:

1. Browser:
   {BASE_URL}/predict

2. Interactive Docs:
   {BASE_URL}/docs

3. curl (GET):
   curl {BASE_URL}/predict

4. curl (POST):
   curl -X POST {BASE_URL}/predict \\
     -H "Content-Type: application/json" \\
     -d '{{"size": 100, "bedrooms": 3, "garden": 1}}'

5. Python:
   import requests
   response = requests.get("{BASE_URL}/predict")
   print(response.json())

📨 Share these URLs with a colleague and ask them to test!
   They should be able to access from anywhere in the world 🌍
""")


def main():
    print("\n" + "="*70)
    print("  ☁️  CLOUD VM DEPLOYMENT TEST SUITE")
    print("="*70)
    print(f"\nTesting service on cloud VM: {VM_HOST}:{VM_PORT}")
    print(f"Full URL: {BASE_URL}")
    
    # Run tests
    results = []
    
    if not test_connection():
        print("\n" + "="*70)
        print("  ❌ CANNOT CONNECT TO SERVICE")
        print("="*70)
        print("\n⚠️  Please ensure:")
        print(f"   1. Container is running on {VM_HOST}")
        print(f"   2. Port {VM_PORT} is correct")
        print(f"   3. Firewall allows connections")
        print(f"\n💡 Check with:")
        print(f"   ssh ubuntu@{VM_HOST}")
        print(f"   docker ps")
        print(f"   docker logs house-api")
        sys.exit(1)
    
    results.append(("GET /predict", test_get_predict()))
    results.append(("POST /predict", test_post_predict()))
    results.append(("Health Check", test_health()))
    results.append(("Multiple Predictions", test_multiple_predictions()))
    
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
        print("\n🎉 All tests passed! Your service is live on the cloud!")
        share_info()
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    # Allow custom port from command line
    if len(sys.argv) > 1:
        VM_PORT = int(sys.argv[1])
        BASE_URL = f"http://{VM_HOST}:{VM_PORT}"
        print(f"Using custom port: {VM_PORT}")
    
    exit_code = main()
    sys.exit(exit_code)

