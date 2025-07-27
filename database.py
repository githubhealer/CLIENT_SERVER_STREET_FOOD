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
