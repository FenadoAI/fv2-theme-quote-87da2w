import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

import requests
import json

# Test the quote generator API
API_BASE = "http://localhost:8001"
API = f"{API_BASE}/api"

def test_quote_generation():
    """Test the quote generation endpoint"""
    print("Testing Quote Generator API...")

    test_data = {
        "theme": "motivation",
        "count": 2
    }

    try:
        response = requests.post(f"{API}/quotes/generate", json=test_data, timeout=30)

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("Response:")
            print(json.dumps(data, indent=2))

            if data.get("success"):
                print(f"\n✅ Successfully generated {len(data.get('quotes', []))} quotes about '{data.get('theme')}'")

                for i, quote in enumerate(data.get('quotes', []), 1):
                    print(f"\nQuote {i}:")
                    print(f'  Text: "{quote.get("text")}"')
                    print(f'  Author: {quote.get("author")}')
                    print(f'  Theme: {quote.get("theme")}')
            else:
                print(f"❌ API returned error: {data.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)

    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        print("Make sure the backend server is running on port 8001")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print("Response:", response.text)

def test_different_themes():
    """Test multiple themes"""
    themes = ["success", "friendship", "wisdom", "courage"]

    print("\n" + "="*50)
    print("Testing Multiple Themes...")
    print("="*50)

    for theme in themes:
        print(f"\nTesting theme: {theme}")
        test_data = {"theme": theme, "count": 1}

        try:
            response = requests.post(f"{API}/quotes/generate", json=test_data, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("quotes"):
                    quote = data["quotes"][0]
                    print(f'  ✅ "{quote["text"]}" - {quote["author"]}')
                else:
                    print(f"  ❌ Failed: {data.get('error', 'No quotes generated')}")
            else:
                print(f"  ❌ HTTP {response.status_code}")

        except Exception as e:
            print(f"  ❌ Error: {e}")

if __name__ == "__main__":
    test_quote_generation()
    test_different_themes()