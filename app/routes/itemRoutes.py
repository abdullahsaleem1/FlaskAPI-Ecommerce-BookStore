from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

# This blueprint is for Order Items (deprecated - use OrderRoutes instead)
# Kept for backward compatibility
items_bp = Blueprint('items', __name__)

@items_bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    """Deprecated: Use /api/v1/admin/orders or /api/v1/orders instead"""
    return jsonify({
        'message': 'This endpoint is deprecated. Use /api/v1/orders instead'
    }), 410

@items_bp.route('/items/<item_id>', methods=['GET'])
@jwt_required()
def get_item(item_id):
    """Deprecated: Use /api/v1/orders/<order_id> instead"""
    return jsonify({
        'message': 'This endpoint is deprecated. Use /api/v1/orders/<order_id> instead'
    }), 410

@items_bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    """Deprecated: Use /api/v1/orders/checkout instead"""
    return jsonify({
        'message': 'This endpoint is deprecated. Use /api/v1/orders/checkout instead'
    }), 410
