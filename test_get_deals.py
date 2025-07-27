"""
Test script for the Get Deals API endpoint
This simulates vendors viewing available deals
"""

import requests
import json

# API endpoint
API_URL = "http://127.0.0.1:5001/api/deals"

def test_get_deals():
    print("🛒 Testing Get Deals API...")
    print("=" * 50)
    
    # Test case 1: Get all active deals
    print("1. Testing get all active deals...")
    try:
        response = requests.get(API_URL, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print(f"   ✅ Success: Found {result['count']} active deals")
                
                # Display first few deals
                for i, deal in enumerate(result['deals'][:3]):
                    print(f"   Deal {i+1}:")
                    print(f"     • {deal['item']} - ₹{deal['price']}/{deal['unit']}")
                    print(f"     • Supplier: {deal['supplier_name']}")
                    print(f"     • Progress: {deal['current_quantity']}/{deal['target_quantity']} ({deal['progress_percentage']}%)")
                    print(f"     • Remaining: {deal['remaining_quantity']} {deal['unit']}")
                    if deal.get('hours_until_expiry'):
                        print(f"     • Expires in: {deal['hours_until_expiry']} hours")
                    print()
            else:
                print(f"   ❌ API Error: {result.get('error')}")
        else:
            result = response.json() if response.content else {'error': 'No response'}
            print(f"   ❌ HTTP Error: {result.get('error', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Error: Cannot connect to Flask server. Make sure it's running on port 5001")
        return
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 2: Filter by location
    print("2. Testing location filtering...")
    try:
        response = requests.get(f"{API_URL}?location=jayanagar", timeout=10)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200 and result['success']:
            print(f"   ✅ Found {result['count']} deals in Jayanagar area")
            print(f"   Filter applied: {result['filters']['location']}")
        else:
            print(f"   ❌ Error: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test case 3: Get all deals (including confirmed/expired)
    print("3. Testing get all deals (any status)...")
    try:
        response = requests.get(f"{API_URL}?status=all", timeout=10)
        result = response.json()
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200 and result['success']:
            print(f"   ✅ Found {result['count']} total deals (all statuses)")
            
            # Count by status
            statuses = {}
            for deal in result['deals']:
                status = deal['status']
                statuses[status] = statuses.get(status, 0) + 1
            
            print("   Deal breakdown by status:")
            for status, count in statuses.items():
                print(f"     • {status}: {count} deals")
        else:
            print(f"   ❌ Error: {result.get('error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    print("✅ Get Deals API test completed!")
    print("\nAPI Usage Examples:")
    print(f"• All active deals: GET {API_URL}")
    print(f"• Filter by location: GET {API_URL}?location=koramangala")
    print(f"• All deals: GET {API_URL}?status=all")
    print(f"• Combined filters: GET {API_URL}?status=active&location=jayanagar")

if __name__ == "__main__":
    test_get_deals()
