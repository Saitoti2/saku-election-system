#!/usr/bin/env python3
"""
Test script to verify health check endpoint
"""
import requests
import json
import sys

def test_health_check():
    """Test the health check endpoint"""
    try:
        # Test local development server
        response = requests.get('http://localhost:8001/', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health Check PASSED")
            print(f"Status: {data.get('status')}")
            print(f"Message: {data.get('message')}")
            print(f"Port: {data.get('port')}")
            print(f"Debug: {data.get('debug')}")
            return True
        else:
            print(f"❌ Health Check FAILED - Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Health Check FAILED - Cannot connect to server")
        print("Make sure Django server is running on port 8001")
        return False
    except requests.exceptions.Timeout:
        print("❌ Health Check FAILED - Request timeout")
        return False
    except json.JSONDecodeError:
        print("❌ Health Check FAILED - Invalid JSON response")
        print(f"Response: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Health Check FAILED - Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing SAKU Election System Health Check...")
    print("=" * 50)
    
    success = test_health_check()
    
    print("=" * 50)
    if success:
        print("🎉 Health check is working correctly!")
        print("✅ Ready for Railway deployment")
        sys.exit(0)
    else:
        print("💥 Health check failed!")
        print("❌ Fix issues before deploying to Railway")
        sys.exit(1)
