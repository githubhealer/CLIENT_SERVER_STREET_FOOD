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
        required_fields = ['supplierName', 'item', 'unit', 'price', 'target_quantity', 'location']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get or create supplier
        supplier_id = db.get_or_create_supplier(data['supplierName'], data['location'])
        
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
            'supplierId': supplier_id,
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

@app.route('/api/deals/<deal_id>/join', methods=['POST'])
def join_deal(deal_id):
    """Join a deal (for vendors)"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['vendorName', 'vendorLocation', 'quantity']
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Get or create vendor
        vendor_id = db.get_or_create_vendor(data['vendorName'], data['vendorLocation'])
        
        # Validate deal exists and is active
        deal = db.get_deal_by_id(deal_id)
        if not deal:
            return jsonify({
                'success': False,
                'error': 'Deal not found'
            }), 404
        
        if deal.get('status') != 'active':
            return jsonify({
                'success': False,
                'error': f'Deal is {deal.get("status", "inactive")} and cannot be joined'
            }), 400
        
        # Validate quantity
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Invalid quantity'
            }), 400
        
        # Check if quantity is available
        remaining = deal['target_quantity'] - deal['current_quantity']
        if quantity > remaining:
            return jsonify({
                'success': False,
                'error': f'Not enough quantity available. Only {remaining} {deal["unit"]} remaining'
            }), 400
        
        # Generate unique order ID
        order_id = f"order_{str(uuid.uuid4())[:8]}"
        
        # Create order object
        new_order = {
            'orderId': order_id,
            'dealId': deal_id,
            'vendorId': vendor_id,
            'quantity': quantity,
            'created_at': datetime.now().isoformat() + "Z"
        }
        
        # Add order to database
        order_success = db.add_order(new_order)
        if not order_success:
            return jsonify({
                'success': False,
                'error': 'Failed to save order to database'
            }), 500
        
        # Update deal's current quantity
        updated_deal = deal.copy()
        updated_deal['current_quantity'] += quantity
        
        # Check if deal target is reached
        if updated_deal['current_quantity'] >= updated_deal['target_quantity']:
            updated_deal['status'] = 'confirmed'
            updated_deal['confirmed_at'] = datetime.now().isoformat() + "Z"
        
        # Update deal in database  
        deal_success = db.update_deal(deal_id, updated_deal)
        if not deal_success:
            return jsonify({
                'success': False,
                'error': 'Failed to update deal'
            }), 500
        
        # Prepare response
        response_data = {
            'success': True,
            'message': 'Successfully joined the deal!',
            'order': new_order,
            'deal_update': {
                'current_quantity': updated_deal['current_quantity'],
                'target_quantity': updated_deal['target_quantity'],
                'remaining_quantity': updated_deal['target_quantity'] - updated_deal['current_quantity'],
                'status': updated_deal['status'],
                'progress_percentage': round((updated_deal['current_quantity'] / updated_deal['target_quantity']) * 100, 1)
            }
        }
        
        # Add confirmation message if deal is complete
        if updated_deal['status'] == 'confirmed':
            response_data['message'] = 'Deal completed! You were part of reaching the target quantity.'
            response_data['deal_completed'] = True
        
        return jsonify(response_data), 201
        
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
