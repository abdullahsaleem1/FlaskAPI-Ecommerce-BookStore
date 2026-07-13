from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.CategoryService import CategoryService
from app.utils.enums import is_admin

category_bp = Blueprint("categories", __name__)
category_service = CategoryService()

# GET /categories - Get all categories
@category_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        # Check for search query parameter
        search = request.args.get('search')
        if search:
            categories = category_service.search_categories(search)
        else:
            categories = category_service.get_all_categories()
        
        return jsonify({
            'success': True,
            'data': categories,
            'message': 'Categories retrieved successfully',
            'total': len(categories)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve categories'
        }), 500

# GET /categories/<category_id> - Get category by ID
@category_bp.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    """Get category by ID"""
    try:
        category = category_service.get_category_by_id(category_id)
        if not category:
            return jsonify({
                'success': False,
                'error': 'Category not found',
                'message': 'Category not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': category,
            'message': 'Category retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve category'
        }), 500

# POST /categories - Create category (Admin only)
@category_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create new category - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        data = request.get_json()
        if not data.get('category_type'):
            return jsonify({
                'success': False,
                'error': 'Category type is required',
                'message': 'Missing required field'
            }), 400
        
        category = category_service.create_category(data)
        return jsonify({
            'success': True,
            'data': category,
            'message': 'Category created successfully'
        }), 201
        
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
            'message': 'Failed to create category'
        }), 500

# PUT /categories/<category_id> - Update category (Admin only)
@category_bp.route('/categories/<category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update category - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        data = request.get_json()
        category = category_service.update_category(category_id, data)
        
        if not category:
            return jsonify({
                'success': False,
                'error': 'Category not found',
                'message': 'Category not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': category,
            'message': 'Category updated successfully'
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
            'message': 'Failed to update category'
        }), 500

# DELETE /categories/<category_id> - Delete category (Admin only)
@category_bp.route('/categories/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete category - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        success = category_service.delete_category(category_id)
        if not success:
            return jsonify({
                'success': False,
                'error': 'Category not found',
                'message': 'Category not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Category deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to delete category'
        }), 500
