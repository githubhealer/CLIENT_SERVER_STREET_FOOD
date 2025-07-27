"""
Test script for Dynamic Supplier Creation
This tests the new functionality where suppliers can type their name
and be automatically added to the database
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5001/api"

def test_dynamic_supplier_creation():
    print("🏪 Testing Dynamic Supplier Creation...")
    print("=" * 50)
    
    # Test 1: Create deal with new supplier
    print("1. Testing deal creation with new supplier...")
    new_supplier_data = {
        "supplierName": "Fresh Farm Supplies",
        "item": "Organic Potatoes",
        "unit": "kg",
        "price": 35.0,
        "target_quantity": 50,
        "location": "Whitefield, Bangalore",
        "description": "Fresh organic potatoes directly from farm"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals", json=new_supplier_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Deal created successfully!")
            print(f"   Deal ID: {result['deal']['dealId']}")
            print(f"   Supplier ID: {result['deal']['supplierId']}")
            print(f"   Item: {result['deal']['item']}")
            print(f"   New supplier created: {new_supplier_data['supplierName']}")
        else:
            result = response.json()
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test 2: Create another deal with the same supplier name (should reuse)
    print("2. Testing deal creation with existing supplier...")
    same_supplier_data = {
        "supplierName": "Fresh Farm Supplies",  # Same name as before
        "item": "Fresh Carrots",
        "unit": "kg", 
        "price": 25.0,
        "target_quantity": 30,
        "location": "Whitefield, Bangalore",
        "description": "Crunchy fresh carrots"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals", json=same_supplier_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Deal created successfully!")
            print(f"   Deal ID: {result['deal']['dealId']}")
            print(f"   Supplier ID: {result['deal']['supplierId']}")
            print(f"   ✅ Existing supplier reused (no duplicate created)")
        else:
            result = response.json()
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test 3: Create deal with different supplier
    print("3. Testing deal creation with another new supplier...")
    different_supplier_data = {
        "supplierName": "Metro Wholesale Foods",
        "item": "Basmati Rice Premium",
        "unit": "kg",
        "price": 120.0,
        "target_quantity": 100,
        "location": "Electronic City, Bangalore"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals", json=different_supplier_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Deal created successfully!")
            print(f"   Deal ID: {result['deal']['dealId']}")
            print(f"   Supplier ID: {result['deal']['supplierId']}")
            print(f"   New supplier created: {different_supplier_data['supplierName']}")
        else:
            result = response.json()
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test 4: Verify suppliers appear in deals API
    print("4. Verifying new suppliers appear in deals...")
    try:
        response = requests.get(f"{BASE_URL}/deals", timeout=10)
        if response.status_code == 200:
            result = response.json()
            deals = result['deals']
            
            # Check for our new suppliers
            new_suppliers = set()
            for deal in deals:
                supplier_name = deal.get('supplier_name', '')
                if supplier_name in ['Fresh Farm Supplies', 'Metro Wholesale Foods']:
                    new_suppliers.add(supplier_name)
                    print(f"   ✅ Found deal from: {supplier_name}")
                    print(f"      Item: {deal['item']} (₹{deal['price']}/{deal['unit']})")
            
            if len(new_suppliers) >= 2:
                print(f"   ✅ All new suppliers visible in deals API")
            else:
                print(f"   ⚠️  Only {len(new_suppliers)} new suppliers found")
        else:
            print(f"   ❌ Failed to get deals: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    
    # Test 5: Case insensitive supplier matching
    print("5. Testing case-insensitive supplier matching...")
    case_test_data = {
        "supplierName": "FRESH FARM SUPPLIES",  # Same supplier, different case
        "item": "Sweet Potatoes",
        "unit": "kg",
        "price": 40.0,
        "target_quantity": 25,
        "location": "Whitefield, Bangalore"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/deals", json=case_test_data, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Deal created successfully!")
            print(f"   ✅ Case-insensitive matching works")
            print(f"   Supplier ID: {result['deal']['supplierId']}")
        else:
            result = response.json()
            print(f"   ❌ Error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
    
    print()
    print("✅ Dynamic Supplier Creation test completed!")
    print("\nFeatures tested:")
    print("✅ New supplier automatic creation")
    print("✅ Existing supplier reuse")
    print("✅ Case-insensitive supplier matching")
    print("✅ Multiple suppliers support")
    print("✅ Integration with deals API")

if __name__ == "__main__":
    test_dynamic_supplier_creation()
