"""
Step 8 - Complete Test: Vendor Join Deal Frontend UI
This validates the complete frontend-to-backend join deal workflow
"""

import requests

BASE_URL = "http://127.0.0.1:5001/api"

def test_step8_complete():
    print("🎯 STEP 8 - COMPLETE TEST: Vendor Join Deal Frontend UI")
    print("=" * 60)
    
    print("✅ Testing Prerequisites:")
    print("   1. Flask server running on http://127.0.0.1:5001/")
    print("   2. Database with active deals available")
    print("   3. Modal UI components in place")
    print("   4. JavaScript event handlers configured")
    
    print("\n🧪 Backend API Validation:")
    
    # Test 1: Verify API endpoint responds correctly
    try:
        response = requests.get(f"{BASE_URL}/deals", timeout=5)
        if response.status_code == 200:
            data = response.json()
            active_deals = [d for d in data['deals'] if d['remaining_quantity'] > 0]
            print(f"   ✅ GET /api/deals: {len(active_deals)} joinable deals available")
        else:
            print(f"   ❌ GET /api/deals: Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ GET /api/deals: Connection error - {str(e)}")
        return False
    
    # Test 2: Test join deal API with frontend data format
    if active_deals:
        test_deal = active_deals[0]
        deal_id = test_deal['dealId']
        
        print(f"\n   Testing deal: {test_deal['item']} (ID: {deal_id[:20]}...)")
        
        # Test the exact payload that frontend sends
        frontend_payload = {
            "vendorId": "vendor_03",  # Anil's Pav Bhaji
            "quantity": 5
        }
        
        try:
            response = requests.post(f"{BASE_URL}/deals/{deal_id}/join", 
                                   json=frontend_payload, timeout=5)
            if response.status_code == 201:
                result = response.json()
                print(f"   ✅ POST /api/deals/{deal_id[:8]}.../join: Success")
                print(f"      Order ID: {result['order']['orderId']}")
                print(f"      Progress: {result['deal_update']['progress_percentage']}%")
            else:
                result = response.json()
                print(f"   ❌ POST join: {result.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"   ❌ POST join: Connection error - {str(e)}")
            return False
    
    print("\n🎨 Frontend UI Components Verification:")
    
    # Verify modal HTML structure exists
    try:
        response = requests.get("http://127.0.0.1:5001/", timeout=5)
        html_content = response.text
        
        # Check for modal components
        modal_checks = [
            ('id="joinDealModal"', 'Join Deal Modal'),
            ('id="joinDealForm"', 'Join Form'),
            ('id="modalDealTitle"', 'Modal Title Display'),
            ('id="joinQuantity"', 'Quantity Input'),
            ('name="vendor_id"', 'Vendor Selection'),
            ('id="submitJoinBtn"', 'Submit Button')
        ]
        
        for check_string, component_name in modal_checks:
            if check_string in html_content:
                print(f"   ✅ {component_name}: Present")
            else:
                print(f"   ❌ {component_name}: Missing")
                return False
                
    except Exception as e:
        print(f"   ❌ Frontend check failed: {str(e)}")
        return False
    
    print("\n🔗 JavaScript Integration Verification:")
    
    # Check for JavaScript functions
    try:
        response = requests.get("http://127.0.0.1:5001/static/js/app.js", timeout=5)
        js_content = response.text
        
        js_checks = [
            ('function openJoinModal', 'Modal Open Function'),
            ('function closeJoinModal', 'Modal Close Function'),
            ('function handleJoinDeal', 'Join Deal Handler'),
            ('setupModalEvents', 'Event Setup Function'),
            ('vendorId:', 'Correct API Field Name')
        ]
        
        for check_string, function_name in js_checks:
            if check_string in js_content:
                print(f"   ✅ {function_name}: Implemented")
            else:
                print(f"   ❌ {function_name}: Missing")
                return False
                
    except Exception as e:
        print(f"   ❌ JavaScript check failed: {str(e)}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 STEP 8 COMPLETE - ALL TESTS PASSED!")
    print("\n📋 Manual Testing Instructions:")
    print("1. Open: http://127.0.0.1:5001/")
    print("2. Click: 'View Available Deals' button")
    print("3. Find any deal with remaining quantity > 0")
    print("4. Click: 'Join Deal' button on that deal")
    print("5. Modal should open with:")
    print("   - Deal title displayed")
    print("   - Vendor dropdown with 4 vendors")
    print("   - Quantity input (min: 1)")
    print("   - 'Join Deal' and 'Cancel' buttons")
    print("6. Select a vendor and quantity, click 'Join Deal'")
    print("7. Success message should appear")
    print("8. Deal progress should update automatically")
    
    print("\n🎯 Expected Behavior:")
    print("✅ Modal opens when clicking 'Join Deal'")
    print("✅ Form validation works (required fields)")
    print("✅ API call succeeds with proper data format")
    print("✅ Success message displays with Order ID")
    print("✅ Deal list refreshes showing updated progress")
    print("✅ Modal closes after successful join")
    
    return True

if __name__ == "__main__":
    success = test_step8_complete()
    if success:
        print("\n🚀 READY FOR STEP 9: Real-time Updates & Notifications!")
    else:
        print("\n⚠️  Fix the issues above before proceeding to Step 9")
