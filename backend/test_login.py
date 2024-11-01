#!/usr/bin/env python3
import requests
import json

def test_login():
    """Test the login endpoint"""
    url = 'http://127.0.0.1:8999/api/auth/login/'
    
    # Test data
    test_cases = [
        {'email': 'admin@college.edu', 'password': 'admin123'},
        {'email': 'student@college.edu', 'password': 'student123'},
        {'email': 'teacher@college.edu', 'password': 'teacher123'},
        {'email': 'resource@college.edu', 'password': 'resource123'}
    ]
    
    print("Testing Campus Connect Login Endpoint")
    print("=" * 50)
    
    for i, credentials in enumerate(test_cases, 1):
        print(f"\nTest {i}: {credentials['email']}")
        print("-" * 30)
        
        try:
            response = requests.post(url, json=credentials)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ Login Successful!")
                print(f"User: {data.get('user', {}).get('first_name', 'N/A')} {data.get('user', {}).get('last_name', 'N/A')}")
                print(f"Role: {data.get('user', {}).get('role', 'N/A')}")
                print(f"Access Token: {data.get('access', 'N/A')[:50]}...")
            else:
                print("❌ Login Failed!")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error - Django server might not be running!")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Login endpoint test completed!")

if __name__ == "__main__":
    test_login()