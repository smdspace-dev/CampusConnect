import requests
import json

# Test the Django backend authentication
def test_login():
    """Test the login endpoint"""
    url = "http://127.0.0.1:8000/api/auth/login/"
    
    # Test with admin credentials
    admin_data = {
        "email": "admin@college.edu",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=admin_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            data = response.json()
            return data.get('access'), data.get('user')
        else:
            print("❌ Login failed!")
            return None, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None

def test_admin_dashboard(access_token):
    """Test the admin dashboard endpoint"""
    if not access_token:
        print("❌ No access token available")
        return
    
    url = "http://127.0.0.1:8000/api/admin_system/dashboard/stats/"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"\nDashboard Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Dashboard access successful!")
            print(f"Dashboard Data: {json.dumps(response.json(), indent=2)}")
        else:
            print("❌ Dashboard access failed!")
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"❌ Dashboard Error: {e}")

if __name__ == "__main__":
    print("🔧 Testing College Management System Backend...")
    print("=" * 50)
    
    # Test login
    access_token, user = test_login()
    
    if access_token:
        print(f"✅ Access Token: {access_token[:50]}...")
        print(f"✅ User: {user}")
        
        # Test dashboard
        test_admin_dashboard(access_token)
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")