"""
Database module for Group-Buying Application
Handles all database operations with JSON file storage
"""

import json
import os
from typing import Dict, List, Optional

class DatabaseManager:
    def __init__(self, db_file: str = 'database.json'):
        self.db_file = db_file
        self._ensure_database_exists()
    
    def _ensure_database_exists(self):
        """Ensure the database file exists with proper structure"""
        if not os.path.exists(self.db_file):
            initial_data = {
                "users": [],
                "deals": [],
                "orders": []
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict:
        """Load data from JSON file"""
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading database: {e}")
            return {"users": [], "deals": [], "orders": []}
    
    def _save_data(self, data: Dict) -> bool:
        """Save data to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (OSError, IOError) as e:
            print(f"Error saving database: {e}")
            return False
    
    # Users operations
    def get_all_users(self) -> List[Dict]:
        """Get all users"""
        data = self._load_data()
        return data.get('users', [])
    
    def get_user_by_id(self, uid: str) -> Optional[Dict]:
        """Get a specific user by ID"""
        users = self.get_all_users()
        return next((user for user in users if user['uid'] == uid), None)
    
    def get_users_by_role(self, role: str) -> List[Dict]:
        """Get users by role (supplier or vendor)"""
        users = self.get_all_users()
        return [user for user in users if user.get('role') == role]
    
    def add_supplier(self, supplier_name: str, location: str) -> str:
        """Add a new supplier and return the supplier ID"""
        import uuid
        
        # Generate unique supplier ID
        supplier_id = f"supplier_{str(uuid.uuid4())[:8]}"
        
        # Create supplier data
        supplier_data = {
            "uid": supplier_id,
            "name": supplier_name,
            "role": "supplier",
            "location": location
        }
        
        # Add to database
        data = self._load_data()
        data['users'].append(supplier_data)
        self._save_data(data)
        
        return supplier_id
    
    def get_supplier_by_name(self, supplier_name: str) -> Optional[Dict]:
        """Get supplier by name (case-insensitive)"""
        suppliers = self.get_users_by_role('supplier')
        return next((supplier for supplier in suppliers 
                    if supplier['name'].lower() == supplier_name.lower()), None)
    
    def get_or_create_supplier(self, supplier_name: str, location: str) -> str:
        """Get existing supplier ID or create new supplier and return ID"""
        existing_supplier = self.get_supplier_by_name(supplier_name)
        if existing_supplier:
            return existing_supplier['uid']
        else:
            return self.add_supplier(supplier_name, location)
    
    def add_vendor(self, vendor_name: str, location: str) -> str:
        """Add a new vendor and return the vendor ID"""
        import uuid
        
        # Generate unique vendor ID
        vendor_id = f"vendor_{str(uuid.uuid4())[:8]}"
        
        # Create vendor data
        vendor_data = {
            "uid": vendor_id,
            "name": vendor_name,
            "role": "vendor",
            "location": location
        }
        
        # Add to database
        data = self._load_data()
        data['users'].append(vendor_data)
        self._save_data(data)
        
        return vendor_id
    
    def get_vendor_by_name(self, vendor_name: str) -> Optional[Dict]:
        """Get vendor by name (case-insensitive)"""
        vendors = self.get_users_by_role('vendor')
        return next((vendor for vendor in vendors 
                    if vendor['name'].lower() == vendor_name.lower()), None)
    
    def get_or_create_vendor(self, vendor_name: str, location: str) -> str:
        """Get existing vendor ID or create new vendor and return ID"""
        existing_vendor = self.get_vendor_by_name(vendor_name)
        if existing_vendor:
            return existing_vendor['uid']
        else:
            return self.add_vendor(vendor_name, location)
    
    # Deals operations
    def get_all_deals(self) -> List[Dict]:
        """Get all deals"""
        data = self._load_data()
        return data.get('deals', [])
    
    def get_active_deals(self) -> List[Dict]:
        """Get only active deals"""
        deals = self.get_all_deals()
        return [deal for deal in deals if deal.get('status') == 'active']
    
    def get_deal_by_id(self, deal_id: str) -> Optional[Dict]:
        """Get a specific deal by ID"""
        deals = self.get_all_deals()
        return next((deal for deal in deals if deal['dealId'] == deal_id), None)
    
    def add_deal(self, deal_data: Dict) -> bool:
        """Add a new deal"""
        data = self._load_data()
        data['deals'].append(deal_data)
        return self._save_data(data)
    
    def update_deal(self, deal_id: str, updated_deal: Dict) -> bool:
        """Update an existing deal"""
        data = self._load_data()
        deals = data.get('deals', [])
        
        for i, deal in enumerate(deals):
            if deal.get('dealId') == deal_id:
                deals[i] = updated_deal
                return self._save_data(data)
        
        return False  # Deal not found
    
    # Orders operations
    def get_all_orders(self) -> List[Dict]:
        """Get all orders"""
        data = self._load_data()
        return data.get('orders', [])
    
    def get_orders_by_deal(self, deal_id: str) -> List[Dict]:
        """Get orders for a specific deal"""
        orders = self.get_all_orders()
        return [order for order in orders if order.get('dealId') == deal_id]
    
    def add_order(self, order_data: Dict) -> bool:
        """Add a new order"""
        data = self._load_data()
        data['orders'].append(order_data)
        return self._save_data(data)
    
    # Utility methods
    def test_connection(self) -> Dict:
        """Test database connection and return stats"""
        try:
            data = self._load_data()
            return {
                'status': 'success',
                'users_count': len(data.get('users', [])),
                'deals_count': len(data.get('deals', [])),
                'orders_count': len(data.get('orders', [])),
                'active_deals_count': len([d for d in data.get('deals', []) if d.get('status') == 'active'])
            }
        except (OSError, IOError, json.JSONDecodeError) as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Create a global database instance
db = DatabaseManager()
