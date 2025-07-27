"""
Test script for the Create Deal API endpoint
This simulates a supplier creating a new deal
"""

import requests
import json

# API endpoint
API_URL = "http://127.0.0.1:5001/api/deals"

def test_create_deal():
    print("🧪 Testing Create Deal API...")
    print("=" * 50)
    
    # Test case 1: Valid deal creation
    print("1. Testing valid deal creation...")
    test_deal = {
        "supplierId": "supplier_01",  # Reliable Veggies
        "item": "Fresh Tomatoes",
        "unit": "kg",
        "price": 30,
        "target_quantity": 150,
        "location": "Jayanagar, Bangalore",
        "description": "Fresh red tomatoes, perfect for cooking"
    }
    
    try:
        response = requests.post(API_URL, json=test_deal)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Success: {result['message']}")
            print(f"   Deal ID: {result['deal']['dealId']}")
            print(f"   Item: {result['deal']['item']}")
            print(f"   Price: ₹{result['deal']['price']}/{result['deal']['unit']}")
            print(f"   Target: {result['deal']['target_quantity']} {result['deal']['unit']}")
        else:
            result = response.json()
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Error: Cannot connect to Flask server. Make sure it's running on port 5001")
        return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 2: Invalid supplier ID
    print("2. Testing invalid supplier ID...")
    invalid_deal = test_deal.copy()
    invalid_deal["supplierId"] = "invalid_supplier"
    
    try:
        response = requests.post(API_URL, json=invalid_deal)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 3: Missing required field
    print("3. Testing missing required field...")
    incomplete_deal = test_deal.copy()
    del incomplete_deal["price"]  # Remove required field
    
    try:
        response = requests.post(API_URL, json=incomplete_deal)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 400:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 4: Vendor trying to create deal (should fail)
    print("4. Testing vendor creating deal (should fail)...")
    vendor_deal = test_deal.copy()
    vendor_deal["supplierId"] = "vendor_01"  # Raju's Chaat Corner
    
    try:
        response = requests.post(API_URL, json=vendor_deal)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 403:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    print("✅ Create Deal API test completed!")
    print("\nTo test manually:")
    print("Use Postman or curl to send POST requests to:")
    print(f"{API_URL}")
    print("\nExample curl command:")
    print('curl -X POST http://127.0.0.1:5001/api/deals \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"supplierId":"supplier_01","item":"Test Item","unit":"kg","price":25,"target_quantity":100,"location":"Test Location"}\'')

if __name__ == "__main__":
    test_create_deal()
