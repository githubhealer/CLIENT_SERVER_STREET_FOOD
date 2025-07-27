from flask import Flask, render_template, jsonify, request
from database import db
import json
import os
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/test-db')
def test_database():
    """Test database connection endpoint"""
    result = db.test_connection()
    return jsonify(result)

@app.route('/api/deals', methods=['POST'])
def create_deal():
    """Create a new deal (for suppliers)"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['supplierId', 'item', 'unit', 'price', 'target_quantity', 'location']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Validate supplier exists
        supplier = db.get_user_by_id(data['supplierId'])
        if not supplier:
            return jsonify({
                'success': False,
                'error': 'Supplier not found'
            }), 404
        
        if supplier.get('role') != 'supplier':
            return jsonify({
                'success': False,
                'error': 'User is not a supplier'
            }), 403
        
        # Validate numeric fields
        try:
            price = float(data['price'])
            target_quantity = int(data['target_quantity'])
            if price <= 0 or target_quantity <= 0:
                raise ValueError("Price and target quantity must be positive")
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Invalid price or target quantity'
            }), 400
        
        # Generate unique deal ID
        deal_id = f"deal_{data['item'].lower().replace(' ', '_')}_{str(uuid.uuid4())[:8]}"
        
        # Calculate expiration date (7 days from now)
        expires_at = (datetime.now() + timedelta(days=7)).isoformat() + "Z"
        
        # Create deal object
        new_deal = {
            'dealId': deal_id,
            'supplierId': data['supplierId'],
            'item': data['item'].strip(),
            'unit': data['unit'].strip(),
            'price': price,
            'target_quantity': target_quantity,
            'current_quantity': 0,  # Start with 0 orders
            'status': 'active',
            'location': data['location'].strip(),
            'expires_at': expires_at,
            'created_at': datetime.now().isoformat() + "Z"
        }
        
        # Add optional description if provided
        if 'description' in data and data['description']:
            new_deal['description'] = data['description'].strip()
        
        # Save to database
        success = db.add_deal(new_deal)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Deal created successfully',
                'deal': new_deal
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to save deal to database'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/deals', methods=['GET'])
def get_deals():
    """Get all active deals (for vendors)"""
    try:
        # Get query parameters for filtering
        status = request.args.get('status', 'active')  # Default to active deals
        location = request.args.get('location', None)
        
        # Get deals based on status
        if status == 'all':
            deals = db.get_all_deals()
        else:
            deals = db.get_active_deals()
        
        # Filter by location if provided
        if location:
            deals = [deal for deal in deals if location.lower() in deal.get('location', '').lower()]
        
        # Enrich deals with supplier information
        enriched_deals = []
        for deal in deals:
            supplier = db.get_user_by_id(deal['supplierId'])
            enriched_deal = deal.copy()
            
            if supplier:
                enriched_deal['supplier_name'] = supplier.get('name', 'Unknown Supplier')
            else:
                enriched_deal['supplier_name'] = 'Unknown Supplier'
            
            # Calculate progress percentage
            progress = (deal['current_quantity'] / deal['target_quantity']) * 100
            enriched_deal['progress_percentage'] = round(progress, 1)
            
            # Calculate remaining quantity
            enriched_deal['remaining_quantity'] = deal['target_quantity'] - deal['current_quantity']
            
            # Check if deal is expiring soon (within 24 hours)
            try:
                expires_at = datetime.fromisoformat(deal['expires_at'].replace('Z', '+00:00'))
                time_until_expiry = expires_at - datetime.now(expires_at.tzinfo)
                enriched_deal['hours_until_expiry'] = round(time_until_expiry.total_seconds() / 3600, 1)
                enriched_deal['is_expiring_soon'] = time_until_expiry.total_seconds() < 86400  # 24 hours
            except:
                enriched_deal['hours_until_expiry'] = None
                enriched_deal['is_expiring_soon'] = False
            
            enriched_deals.append(enriched_deal)
        
        # Sort deals by creation date (newest first)
        enriched_deals.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'deals': enriched_deals,
            'count': len(enriched_deals),
            'filters': {
                'status': status,
                'location': location
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# Load database helper function (legacy - now using database.py)
def load_database():
    """Load data from database.json file"""
    try:
        with open('database.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": [], "deals": [], "orders": []}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
