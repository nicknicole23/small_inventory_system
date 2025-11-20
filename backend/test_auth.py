#!/usr/bin/env python3
"""
Test script for authentication endpoints.

This script tests the user registration and login functionality.
Make sure the Flask server is running before executing this script.

Usage:
    python test_auth.py
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000/api/auth"
HEADERS = {"Content-Type": "application/json"}


def print_response(response, title):
    """Pretty print API response."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"{'='*60}\n")


def test_register():
    """Test user registration."""
    print("\n🧪 Testing User Registration...")
    
    # Test data
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123",
        "first_name": "John",
        "last_name": "Doe",
        "role": "staff"
    }
    
    response = requests.post(
        f"{BASE_URL}/register",
        headers=HEADERS,
        json=user_data
    )
    
    print_response(response, "User Registration")
    return response


def test_register_admin():
    """Test admin user registration."""
    print("\n🧪 Testing Admin Registration...")
    
    # Test data for admin
    admin_data = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin"
    }
    
    response = requests.post(
        f"{BASE_URL}/register",
        headers=HEADERS,
        json=admin_data
    )
    
    print_response(response, "Admin Registration")
    return response


def test_duplicate_registration():
    """Test duplicate user registration (should fail)."""
    print("\n🧪 Testing Duplicate Registration (Should Fail)...")
    
    user_data = {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "password123"
    }
    
    response = requests.post(
        f"{BASE_URL}/register",
        headers=HEADERS,
        json=user_data
    )
    
    print_response(response, "Duplicate Registration (Expected to Fail)")
    return response


def test_login(email="john@example.com", password="password123"):
    """Test user login."""
    print("\n🧪 Testing User Login...")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(
        f"{BASE_URL}/login",
        headers=HEADERS,
        json=login_data
    )
    
    print_response(response, "User Login")
    
    if response.status_code == 200:
        data = response.json()
        return data.get('access_token'), data.get('refresh_token')
    
    return None, None


def test_invalid_login():
    """Test login with invalid credentials (should fail)."""
    print("\n🧪 Testing Invalid Login (Should Fail)...")
    
    login_data = {
        "email": "john@example.com",
        "password": "wrongpassword"
    }
    
    response = requests.post(
        f"{BASE_URL}/login",
        headers=HEADERS,
        json=login_data
    )
    
    print_response(response, "Invalid Login (Expected to Fail)")
    return response


def test_get_current_user(access_token):
    """Test getting current user info."""
    print("\n🧪 Testing Get Current User...")
    
    if not access_token:
        print("❌ No access token available. Skipping test.")
        return None
    
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.get(
        f"{BASE_URL}/me",
        headers=headers
    )
    
    print_response(response, "Get Current User")
    return response


def test_refresh_token(refresh_token):
    """Test token refresh."""
    print("\n🧪 Testing Token Refresh...")
    
    if not refresh_token:
        print("❌ No refresh token available. Skipping test.")
        return None
    
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {refresh_token}"
    }
    
    response = requests.post(
        f"{BASE_URL}/refresh",
        headers=headers
    )
    
    print_response(response, "Token Refresh")
    
    if response.status_code == 200:
        return response.json().get('access_token')
    
    return None


def test_change_password(access_token):
    """Test password change."""
    print("\n🧪 Testing Password Change...")
    
    if not access_token:
        print("❌ No access token available. Skipping test.")
        return None
    
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {access_token}"
    }
    
    password_data = {
        "current_password": "password123",
        "new_password": "newpassword123"
    }
    
    response = requests.put(
        f"{BASE_URL}/change-password",
        headers=headers,
        json=password_data
    )
    
    print_response(response, "Password Change")
    return response


def test_logout(access_token):
    """Test logout."""
    print("\n🧪 Testing Logout...")
    
    if not access_token:
        print("❌ No access token available. Skipping test.")
        return None
    
    headers = {
        **HEADERS,
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.post(
        f"{BASE_URL}/logout",
        headers=headers
    )
    
    print_response(response, "Logout")
    return response


def main():
    """Run all authentication tests."""
    print("\n" + "="*60)
    print("🚀 AUTHENTICATION ENDPOINTS TEST SUITE")
    print("="*60)
    print("\nMake sure the Flask server is running at http://localhost:5000")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n\n❌ Tests cancelled.")
        return
    
    try:
        # Test 1: Register new user
        test_register()
        
        # Test 2: Register admin user
        test_register_admin()
        
        # Test 3: Try duplicate registration (should fail)
        test_duplicate_registration()
        
        # Test 4: Login with valid credentials
        access_token, refresh_token = test_login()
        
        # Test 5: Login with invalid credentials (should fail)
        test_invalid_login()
        
        # Test 6: Get current user info
        test_get_current_user(access_token)
        
        # Test 7: Refresh access token
        new_access_token = test_refresh_token(refresh_token)
        
        # Test 8: Change password
        test_change_password(access_token if access_token else new_access_token)
        
        # Test 9: Login with new password
        if new_access_token:
            print("\n🧪 Testing Login with New Password...")
            test_login(email="john@example.com", password="newpassword123")
        
        # Test 10: Logout
        test_logout(access_token if access_token else new_access_token)
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("Please make sure the Flask server is running at http://localhost:5000")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
