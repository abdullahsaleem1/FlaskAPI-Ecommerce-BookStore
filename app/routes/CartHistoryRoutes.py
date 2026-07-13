from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.CartHistoryService import CartHistoryService
from app.utils.enums import is_admin

cart_history_bp = Blueprint('cart_history', __name__)
cart_history_service = CartHistoryService()

@cart_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_cart_history():
    """Get all cart history (admin only)"""
    if not is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    cart_histories = cart_history_service.get_all_cart_history()
    return jsonify(cart_histories), 200

@cart_history_bp.route('/<cart_history_id>', methods=['GET'])
@jwt_required()
def get_cart_history(cart_history_id):
    """Get a specific cart history record"""
    cart_history = cart_history_service.get_cart_history(cart_history_id)
    if not cart_history:
        return jsonify({'error': 'Cart history not found'}), 404
    
    user_id = get_jwt_identity()
    if cart_history['user_id'] != user_id and not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(cart_history), 200

@cart_history_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_cart_history(user_id):
    """Get cart history for a user"""
    current_user_id = get_jwt_identity()
    
    # Users can only view their own history unless admin
    if current_user_id != user_id and not is_admin():
        return jsonify({'error': 'Unauthorized'}), 403
    
    cart_histories = cart_history_service.get_user_cart_history(user_id)
    return jsonify(cart_histories), 200

@cart_history_bp.route('/order-item/<order_item_id>', methods=['GET'])
@jwt_required()
def get_order_item_history(order_item_id):
    """Get cart history for an order item"""
    if not is_admin():
        return jsonify({'error': 'Admin access required'}), 403
    
    cart_histories = cart_history_service.get_order_item_history(order_item_id)
    return jsonify(cart_histories), 200
