from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.ReviewService import ReviewService
from app.utils.enums import is_admin

review_bp = Blueprint('reviews', __name__)
review_service = ReviewService()

@review_bp.route('/', methods=['GET'])
def get_all_reviews():
    """Get all reviews"""
    try:
        reviews = review_service.get_all_reviews()
        return jsonify({
            'success': True,
            'data': reviews,
            'total': len(reviews)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/<review_id>', methods=['GET'])
def get_review(review_id):
    """Get a specific review"""
    try:
        review = review_service.get_review(review_id)
        if not review:
            return jsonify({'success': False, 'error': 'Review not found'}), 404
        return jsonify({'success': True, 'data': review}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/book/<book_id>', methods=['GET'])
def get_book_reviews(book_id):
    """Get all reviews for a book"""
    try:
        reviews = review_service.get_book_reviews(book_id)
        return jsonify({
            'success': True,
            'data': reviews,
            'total': len(reviews)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/book/<book_id>/summary', methods=['GET'])
def get_book_rating_summary(book_id):
    """Get rating summary for a book"""
    try:
        summary = review_service.get_book_rating_summary(book_id)
        return jsonify({'success': True, 'data': summary}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/user/<user_id>', methods=['GET'])
@jwt_required()
def get_user_reviews(user_id):
    """Get all reviews by a user"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only view their own reviews unless admin
        if current_user_id != user_id and not is_admin():
            return jsonify({'success': False, 'error': 'Unauthorized'}), 403
        
        reviews = review_service.get_user_reviews(user_id)
        return jsonify({
            'success': True,
            'data': reviews,
            'total': len(reviews)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/', methods=['POST'])
@jwt_required()
def create_review():
    """Create a new review"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        # Validate required fields
        if not data.get('book_id'):
            return jsonify({'success': False, 'error': 'book_id is required'}), 400
        if not data.get('rating'):
            return jsonify({'success': False, 'error': 'rating is required'}), 400
        
        review = review_service.create_review(
            user_id=user_id,
            book_id=data['book_id'],
            rating=data['rating'],
            comment=data.get('comment')
        )
        return jsonify({
            'success': True,
            'message': 'Review created successfully',
            'data': review
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    """Update a review"""
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        
        updated_review = review_service.update_review(review_id, user_id, data)
        if not updated_review:
            return jsonify({'success': False, 'error': 'Review not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Review updated successfully',
            'data': updated_review
        }), 200
    except PermissionError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@review_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """Delete a review"""
    try:
        user_id = get_jwt_identity()
        admin = is_admin()
        
        deleted = review_service.delete_review(review_id, user_id, admin)
        if not deleted:
            return jsonify({'success': False, 'error': 'Review not found'}), 404
        
        return jsonify({
            'success': True,
            'message': 'Review deleted successfully'
        }), 200
    except PermissionError as e:
        return jsonify({'success': False, 'error': str(e)}), 403
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
