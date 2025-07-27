"""
Test script for database module
Run this to verify database connection and operations
"""

from database import db

def test_database_module():
    print("🔍 Testing Database Module...")
    print("=" * 50)
    
    # Test connection
    print("1. Testing database connection...")
    connection_test = db.test_connection()
    print(f"   Status: {connection_test['status']}")
    if connection_test['status'] == 'success':
        print(f"   Users: {connection_test['users_count']}")
        print(f"   Deals: {connection_test['deals_count']}")
        print(f"   Orders: {connection_test['orders_count']}")
        print(f"   Active Deals: {connection_test['active_deals_count']}")
    else:
        print(f"   Error: {connection_test.get('error')}")
    
    print()
    
    # Test reading users
    print("2. Testing user operations...")
    suppliers = db.get_users_by_role('supplier')
    vendors = db.get_users_by_role('vendor')
    print(f"   Suppliers found: {len(suppliers)}")
    print(f"   Vendors found: {len(vendors)}")
    
    if suppliers:
        print(f"   First supplier: {suppliers[0]['name']}")
    
    print()
    
    # Test reading deals
    print("3. Testing deal operations...")
    all_deals = db.get_all_deals()
    active_deals = db.get_active_deals()
    print(f"   Total deals: {len(all_deals)}")
    print(f"   Active deals: {len(active_deals)}")
    
    if active_deals:
        deal = active_deals[0]
        print(f"   First active deal: {deal['item']} - ₹{deal['price']}/{deal['unit']}")
    
    print()
    
    # Test reading orders
    print("4. Testing order operations...")
    all_orders = db.get_all_orders()
    print(f"   Total orders: {len(all_orders)}")
    
    if all_orders:
        order = all_orders[0]
        print(f"   First order: Deal {order['dealId']} - Quantity {order['quantity']}")
    
    print()
    print("✅ Database module test completed!")

if __name__ == "__main__":
    test_database_module()
