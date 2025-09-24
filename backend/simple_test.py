import requests
import json
import time

def test_basic_endpoint():
    """Test the basic health check endpoint"""
    try:
        response = requests.get("http://localhost:8001/api/", timeout=10)
        print(f"Basic endpoint status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Basic endpoint failed: {e}")
    return False

def test_quote_endpoint():
    """Test quote generation with a simple request"""
    try:
        data = {"theme": "success", "count": 1}
        print(f"Testing quote endpoint with data: {data}")

        response = requests.post(
            "http://localhost:8001/api/quotes/generate",
            json=data,
            timeout=60  # Longer timeout for AI processing
        )

        print(f"Quote endpoint status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"Error response: {response.text}")
    except Exception as e:
        print(f"Quote endpoint failed: {e}")
    return False

if __name__ == "__main__":
    print("Testing basic endpoint...")
    basic_works = test_basic_endpoint()

    if basic_works:
        print("\nTesting quote generation...")
        test_quote_endpoint()
    else:
        print("Basic endpoint failed, skipping quote test")