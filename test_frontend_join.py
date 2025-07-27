"""
Test script for the Frontend Join Deal functionality
This tests the complete frontend-to-backend flow
"""

import requests
import time

# API endpoint
BASE_URL = "http://127.0.0.1:5001/api"

def test_frontend_join():
    print("🖥️ Testing Frontend Join Deal Flow...")
    print("=" * 50)
    
    # Step 1: Get available deals
    print("1. Getting available deals to test join functionality...")
    try:
        response = requests.get(f"{BASE_URL}/deals", timeout=10)
        deals_result = response.json()
        if response.status_code == 200 and deals_result['success'] and deals_result['deals']:
            print(f"   ✅ Found {len(deals_result['deals'])} available deals")
            for i, deal in enumerate(deals_result['deals'][:3]):  # Show first 3
                print(f"      {i+1}. {deal['item']} - {deal['remaining_quantity']} {deal['unit']} available")
                print(f"         ID: {deal['dealId']}")
        else:
            print("   ❌ No deals available for testing")
            return False
    except Exception as e:
        print(f"   ❌ Error getting deals: {str(e)}")
        return False
    
    print()
    
    # Step 2: Test the exact data format that frontend will send
    print("2. Testing frontend data format...")
    test_deal = deals_result['deals'][0]
    deal_id = test_deal['dealId']
    min_quantity = 1  # Default minimum quantity
    
    # This mimics exactly what the frontend JavaScript will send
    frontend_data = {
        "vendorId": "vendor_02",  # Sita's Samosa Stall
        "quantity": min_quantity
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals/{deal_id}/join", json=frontend_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Frontend join successful!")
            print(f"   Order ID: {result['order']['orderId']}")
            print(f"   Vendor: {result['order']['vendorId']}")
            print(f"   Quantity: {result['order']['quantity']}")
            print(f"   Deal Progress: {result['deal_update']['progress_percentage']}%")
            return True
        else:
            result = response.json()
            print(f"   ❌ Frontend join failed: {result.get('error', 'Unknown error')}")
            if 'errors' in result:
                for field, error in result['errors'].items():
                    print(f"      {field}: {error}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_modal_data():
    print("\n3. Testing modal data structure...")
    
    # Get deals to check modal data
    try:
        response = requests.get(f"{BASE_URL}/deals", timeout=10)
        deals_result = response.json()
        
        if deals_result['success'] and deals_result['deals']:
            deal = deals_result['deals'][0]
            print(f"   Deal for modal testing:")
            print(f"   - ID: {deal['dealId']}")
            print(f"   - Title: {deal['item']}")
            print(f"   - Min Quantity: 1 (default)")
            print(f"   ✅ Modal data structure ready")
            
            # Test if openJoinModal would have correct parameters
            print(f"   JavaScript call would be:")
            print(f"   openJoinModal('{deal['dealId']}', '{deal['item']}', 1)")
            return True
        else:
            print("   ❌ No deals for modal testing")
            return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success1 = test_frontend_join()
    success2 = test_modal_data()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("✅ All frontend join tests PASSED!")
        print("🎉 Ready for manual UI testing!")
    else:
        print("❌ Some tests FAILED - check the issues above")
    
    print("\nNext steps:")
    print("1. Open http://127.0.0.1:5001/ in browser")
    print("2. Click 'View Available Deals'")
    print("3. Click 'Join Deal' button on any active deal")
    print("4. Fill the modal form and submit")
