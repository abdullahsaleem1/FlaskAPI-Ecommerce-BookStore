from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.OrderService import OrderService
from app.utils.enums import is_admin

order_bp = Blueprint("orders", __name__)
order_service = OrderService()

# POST /orders/checkout - Create order from cart
@order_bp.route('/orders/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """Checkout - Create order from cart"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate shipping data
        if not data.get('shipping_address') or not data.get('city') or not data.get('phone_number'):
            return jsonify({
                'success': False,
                'error': 'Shipping address, city, and phone number are required',
                'message': 'Missing required fields'
            }), 400
        
        order = order_service.create_order_from_cart(current_user_id, data)
        
        return jsonify({
            'success': True,
            'data': order,
            'message': 'Order created successfully'
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Validation error'
        }), 400
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Permission denied'
        }), 403
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to create order'
        }), 500

# GET /orders - Get current user's orders
@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    """Get all orders for current user"""
    try:
        current_user_id = get_jwt_identity()
        orders = order_service.get_user_orders(current_user_id)
        
        return jsonify({
            'success': True,
            'data': orders,
            'message': 'Orders retrieved successfully',
            'total': len(orders)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve orders'
        }), 500

# GET /orders/recent - Get recent orders
@order_bp.route('/orders/recent', methods=['GET'])
@jwt_required()
def get_recent_orders():
    """Get recent orders for current user"""
    try:
        current_user_id = get_jwt_identity()
        limit = request.args.get('limit', 5, type=int)
        orders = order_service.get_recent_orders(current_user_id, limit)
        
        return jsonify({
            'success': True,
            'data': orders,
            'message': 'Recent orders retrieved successfully',
            'total': len(orders)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve recent orders'
        }), 500

# GET /orders/<order_id> - Get order details
@order_bp.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details by ID"""
    try:
        current_user_id = get_jwt_identity()
        
        # Admins can view any order, users can only view their own
        if is_admin():
            order = order_service.get_order_details(order_id)
        else:
            order = order_service.get_order_details(order_id, current_user_id)
        
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found',
                'message': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': order,
            'message': 'Order retrieved successfully'
        }), 200
        
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Permission denied'
        }), 403
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve order'
        }), 500

# GET /admin/orders - Get all orders (Admin only)
@order_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    """Get all orders - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        # Check if filtering by status
        status = request.args.get('status')
        if status:
            orders = order_service.get_orders_by_status(status)
        else:
            orders = order_service.get_all_orders()
        
        return jsonify({
            'success': True,
            'data': orders,
            'message': 'Orders retrieved successfully',
            'total': len(orders)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve orders'
        }), 500

# PUT /admin/orders/<order_id>/status - Update order status (Admin only)
@order_bp.route('/admin/orders/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        data = request.get_json()
        status = data.get('status')
        
        if not status:
            return jsonify({
                'success': False,
                'error': 'Status is required',
                'message': 'Missing required field'
            }), 400
        
        order = order_service.update_order_status(order_id, status)
        
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found',
                'message': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': order,
            'message': 'Order status updated successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Validation error'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update order status'
        }), 500

# PUT /admin/orders/<order_id>/tracking - Update tracking number (Admin only)
@order_bp.route('/admin/orders/<order_id>/tracking', methods=['PUT'])
@jwt_required()
def update_tracking_number(order_id):
    """Update order tracking number - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        data = request.get_json()
        tracking_number = data.get('tracking_number')
        
        if not tracking_number:
            return jsonify({
                'success': False,
                'error': 'Tracking number is required',
                'message': 'Missing required field'
            }), 400
        
        order = order_service.update_tracking_number(order_id, tracking_number)
        
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found',
                'message': 'Order not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': order,
            'message': 'Tracking number updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update tracking number'
        }), 500

# POST /orders/<order_id>/cancel - Cancel order
@order_bp.route('/orders/<order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order"""
    try:
        current_user_id = get_jwt_identity()
        admin = is_admin()
        
        order = order_service.cancel_order(order_id, current_user_id, is_admin=admin)
        
        return jsonify({
            'success': True,
            'data': order,
            'message': 'Order cancelled successfully'
        }), 200
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Validation error'
        }), 400
    except PermissionError as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Permission denied'
        }), 403
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to cancel order'
        }), 500
