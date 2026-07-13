from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.AuthorService import AuthorService
from app.utils.enums import is_admin

author_bp = Blueprint("authors", __name__)
author_service = AuthorService()

# GET /authors - Get all authors
@author_bp.route('/authors', methods=['GET'])
def get_authors():
    """Get all authors"""
    try:
        search = request.args.get('search')
        if search:
            authors = author_service.search_authors(search)
        else:
            authors = author_service.get_all_authors()
        
        return jsonify({
            'success': True,
            'data': authors,
            'message': 'Authors retrieved successfully',
            'total': len(authors)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve authors'
        }), 500

# GET /authors/name/<author_name> - Get author by name
@author_bp.route('/authors/name/<author_name>', methods=['GET'])
def get_author(author_name):
    """Get author by name"""
    try:
        print(f"DEBUG: Received author_name parameter: '{author_name}'")
        author = author_service.get_author_by_name(author_name)
        print(f"DEBUG: Author result: {author}")
        if not author:
            return jsonify({
                'success': False,
                'error': 'Author not found',
                'message': 'Author not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': author,
            'message': 'Author retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve author'
        }), 500

# POST /authors - Create author (Admin only)
@author_bp.route('/authors', methods=['POST'])
@jwt_required()
def create_author():
    """Create new author - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        data = request.get_json()
        if not data.get('author_name'):
            return jsonify({
                'success': False,
                'error': 'Author name is required',
                'message': 'Missing required field'
            }), 400
        
        author = author_service.create_author(data)
        return jsonify({
            'success': True,
            'data': author,
            'message': 'Author created successfully'
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
            'message': 'Failed to create author'
        }), 500

# PUT /authors/<author_name> - Update author (Admin only)
@author_bp.route('/authors/<author_name>', methods=['PUT'])
@jwt_required()
def update_author(author_name):
    """Update author - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        data = request.get_json()
        author = author_service.update_author(author_name, data)
        
        if not author:
            return jsonify({
                'success': False,
                'error': 'Author not found',
                'message': 'Author not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': author,
            'message': 'Author updated successfully'
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
            'message': 'Failed to update author'
        }), 500

# DELETE /authors/name/<author_name> - Delete author by name (Admin only)
@author_bp.route('/authors/name/<author_name>', methods=['DELETE'])
@jwt_required()
def delete_author(author_name):
    """Delete author by name - Admin only"""
    try:
        if not is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin access required',
                'message': 'Permission denied'
            }), 403
        
        if not author_name:
            return jsonify({
                'success': False,
                'error': 'Author name is required',
                'message': 'Missing required field'
            }), 400
            
        success = author_service.delete_author(author_name)
        if not success:
            return jsonify({
                'success': False,
                'error': 'Author not found',
                'message': 'Author not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Author deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to delete author'
        }), 500

