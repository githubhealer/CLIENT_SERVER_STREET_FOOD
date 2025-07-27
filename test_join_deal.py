"""
Test script for the Join Deal API endpoint
This simulates vendors joining deals
"""

import requests

# API endpoint
BASE_URL = "http://127.0.0.1:5001/api"

def test_join_deal():
    print("🤝 Testing Join Deal API...")
    print("=" * 50)
    
    # First, get available deals to test with
    print("0. Getting available deals...")
    try:
        response = requests.get(f"{BASE_URL}/deals", timeout=10)
        deals_result = response.json()
        if response.status_code == 200 and deals_result['success'] and deals_result['deals']:
            test_deal = deals_result['deals'][0]  # Use first deal
            deal_id = test_deal['dealId']
            print(f"   Using deal: {test_deal['item']} (ID: {deal_id})")
            print(f"   Available: {test_deal['remaining_quantity']} {test_deal['unit']}")
        else:
            print("   ❌ No deals available for testing")
            return
    except Exception as e:
        print(f"   ❌ Error getting deals: {str(e)}")
        return
    
    print()
    
    # Test case 1: Valid join request
    print("1. Testing valid join request...")
    join_data = {
        "vendorId": "vendor_01",  # Raju's Chaat Corner
        "quantity": 10
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals/{deal_id}/join", json=join_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Success: {result['message']}")
            print(f"   Order ID: {result['order']['orderId']}")
            print(f"   Quantity: {result['order']['quantity']}")
            print(f"   Deal Progress: {result['deal_update']['current_quantity']}/{result['deal_update']['target_quantity']} ({result['deal_update']['progress_percentage']}%)")
            if result.get('deal_completed'):
                print("   🎉 Deal completed!")
        else:
            result = response.json()
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 2: Invalid vendor ID
    print("2. Testing invalid vendor ID...")
    invalid_data = {
        "vendorId": "invalid_vendor",
        "quantity": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals/{deal_id}/join", json=invalid_data, timeout=10)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 3: Supplier trying to join deal
    print("3. Testing supplier trying to join deal...")
    supplier_data = {
        "vendorId": "supplier_01",  # Reliable Veggies (supplier, not vendor)
        "quantity": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals/{deal_id}/join", json=supplier_data, timeout=10)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 403:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 4: Missing required field
    print("4. Testing missing required field...")
    incomplete_data = {
        "vendorId": "vendor_02"
        # Missing quantity
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals/{deal_id}/join", json=incomplete_data, timeout=10)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 400:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 5: Invalid deal ID
    print("5. Testing invalid deal ID...")
    valid_data = {
        "vendorId": "vendor_02",
        "quantity": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals/invalid_deal_id/join", json=valid_data, timeout=10)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 404:
            print(f"   ✅ Correctly rejected: {result['error']}")
        else:
            print(f"   ❌ Unexpected result: {result}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    print("✅ Join Deal API test completed!")
    print("\nAPI Usage Example:")
    print(f'curl -X POST {BASE_URL}/deals/{{deal_id}}/join \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"vendorId":"vendor_01","quantity":10}\'')

if __name__ == "__main__":
    test_join_deal()
