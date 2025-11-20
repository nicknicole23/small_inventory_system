#!/usr/bin/env python3
"""
Test login functionality
"""
import requests
import json

# Backend URL
BASE_URL = "http://localhost:5000/api"

def test_login():
    """Test the login endpoint"""
    print("Testing login endpoint...")
    print("-" * 50)
    
    # Login credentials
    credentials = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    print(f"Attempting login with: {credentials['email']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json=credentials,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("\n✅ Login successful!")
            data = response.json()
            print(f"Access Token: {data.get('access_token', 'N/A')[:50]}...")
            print(f"User: {data.get('user', {}).get('email')}")
        else:
            print("\n❌ Login failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server!")
        print("Make sure the Flask server is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_login()
