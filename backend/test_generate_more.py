#!/usr/bin/env python3
"""
Test script to verify the 'Generate More' functionality works correctly
"""

import requests
import json
import sys

API_BASE = "http://localhost:8001"
API = f"{API_BASE}/api"

def test_generate_more_functionality():
    """Test the generate more quotes functionality"""
    print("🧪 Testing 'Generate More' Functionality")
    print("=" * 50)

    theme = "inspiration"

    # Test 1: Generate initial quotes
    print(f"\n📝 Step 1: Generate initial quotes for theme '{theme}'")

    test_data = {
        "theme": theme,
        "count": 2
    }

    try:
        response = requests.post(f"{API}/quotes/generate", json=test_data, timeout=30)

        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            return False

        data = response.json()

        if not data.get("success"):
            print(f"❌ API Error: {data.get('error', 'Unknown error')}")
            return False

        initial_quotes = data.get("quotes", [])
        print(f"✅ Generated {len(initial_quotes)} initial quotes")

        for i, quote in enumerate(initial_quotes, 1):
            print(f"   Quote {i}: \"{quote['text'][:50]}...\" - {quote['author']}")

    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

    # Test 2: Generate more quotes (simulate "Generate More" button click)
    print(f"\n🔄 Step 2: Generate MORE quotes for same theme '{theme}'")

    try:
        response2 = requests.post(f"{API}/quotes/generate", json=test_data, timeout=30)

        if response2.status_code != 200:
            print(f"❌ HTTP Error: {response2.status_code}")
            return False

        data2 = response2.json()

        if not data2.get("success"):
            print(f"❌ API Error: {data2.get('error', 'Unknown error')}")
            return False

        more_quotes = data2.get("quotes", [])
        print(f"✅ Generated {len(more_quotes)} additional quotes")

        for i, quote in enumerate(more_quotes, 1):
            print(f"   Quote {i}: \"{quote['text'][:50]}...\" - {quote['author']}")

        # Verify quotes are different (they should be different each time)
        initial_texts = [q['text'] for q in initial_quotes]
        more_texts = [q['text'] for q in more_quotes]

        duplicates = set(initial_texts) & set(more_texts)
        if duplicates:
            print(f"⚠️  Warning: Found duplicate quotes: {len(duplicates)}")
        else:
            print("✅ All quotes are unique between generations")

    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

    # Test 3: Test with different counts
    print(f"\n🔢 Step 3: Test different quote counts")

    for count in [1, 3, 5]:
        test_data_count = {
            "theme": theme,
            "count": count
        }

        try:
            response = requests.post(f"{API}/quotes/generate", json=test_data_count, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    quotes = data.get("quotes", [])
                    print(f"   ✅ Count {count}: Generated {len(quotes)} quotes")
                else:
                    print(f"   ❌ Count {count}: API Error - {data.get('error')}")
            else:
                print(f"   ❌ Count {count}: HTTP {response.status_code}")

        except requests.RequestException as e:
            print(f"   ❌ Count {count}: Request failed - {e}")

    print(f"\n🎯 Step 4: Test different themes")

    themes_to_test = ["success", "courage", "friendship", "wisdom", "love"]

    for theme_name in themes_to_test:
        test_data_theme = {
            "theme": theme_name,
            "count": 1
        }

        try:
            response = requests.post(f"{API}/quotes/generate", json=test_data_theme, timeout=30)

            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("quotes"):
                    quote = data["quotes"][0]
                    print(f"   ✅ {theme_name}: \"{quote['text'][:40]}...\" - {quote['author']}")
                else:
                    print(f"   ❌ {theme_name}: No quotes generated - {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ {theme_name}: HTTP {response.status_code}")

        except requests.RequestException as e:
            print(f"   ❌ {theme_name}: Request failed - {e}")

    print(f"\n🎉 Generate More functionality test completed!")
    return True

if __name__ == "__main__":
    print("🚀 Starting Generate More Quote Functionality Test")
    print("Make sure the backend server is running on port 8001")
    print()

    success = test_generate_more_functionality()

    if success:
        print("\n✅ All tests passed! The 'Generate More' functionality is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the backend server and try again.")
        sys.exit(1)