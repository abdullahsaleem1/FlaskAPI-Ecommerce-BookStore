from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.CartService import CartService

cart_bp = Blueprint("cart", __name__)

# GET user's cart
@cart_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get user's cart with all items and book details"""
    try:
        current_user_id = get_jwt_identity()
        cart_items = CartService.get_user_cart(current_user_id)
        
        return jsonify({
            'cart': cart_items,
            'total_items': len(cart_items)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET cart summary
@cart_bp.route('/cart/summary', methods=['GET'])
@jwt_required()
def get_cart_summary():
    """Get cart summary with totals"""
    try:
        current_user_id = get_jwt_identity()
        summary = CartService.get_cart_summary(current_user_id)
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST add item to cart
@cart_bp.route('/cart/items', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to cart or update quantity if already exists"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if not data.get('book_id'):
            return jsonify({'error': 'book_id is required'}), 400
        
        quantity = data.get('quantity', 1)
        
        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid quantity format'}), 400
        
        cart_item = CartService.add_to_cart(
            user_id=current_user_id,
            book_id=data['book_id'],
            quantity=quantity
        )
        
        return jsonify({
            'message': 'Item added to cart successfully',
            'cart_item': cart_item.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT update cart item quantity
@cart_bp.route('/cart/items/<cart_item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(cart_item_id):
    """Update cart item quantity"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate quantity
        if 'quantity' not in data:
            return jsonify({'error': 'quantity is required'}), 400
        
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid quantity format'}), 400
        
        cart_item = CartService.update_cart_item(
            cart_item_id=cart_item_id,
            user_id=current_user_id,
            quantity=quantity
        )
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        return jsonify({
            'message': 'Cart item updated successfully',
            'cart_item': cart_item.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE remove item from cart
@cart_bp.route('/cart/items/<cart_item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(cart_item_id):
    """Remove specific item from cart"""
    try:
        current_user_id = get_jwt_identity()
        success = CartService.remove_from_cart(
            cart_item_id=cart_item_id,
            user_id=current_user_id
        )
        
        if not success:
            return jsonify({'error': 'Cart item not found'}), 404
        
        return jsonify({'message': 'Item removed from cart successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE clear entire cart
@cart_bp.route('/cart', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from user's cart"""
    try:
        current_user_id = get_jwt_identity()
        CartService.clear_cart(current_user_id)
        
        return jsonify({'message': 'Cart cleared successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET specific cart item
@cart_bp.route('/cart/items/<cart_item_id>', methods=['GET'])
@jwt_required()
def get_cart_item(cart_item_id):
    """Get specific cart item details"""
    try:
        current_user_id = get_jwt_identity()
        cart_item = CartService.get_cart_item_by_id(
            cart_item_id=cart_item_id,
            user_id=current_user_id
        )
        
        if not cart_item:
            return jsonify({'error': 'Cart item not found'}), 404
        
        return jsonify({'cart_item': cart_item.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
