from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.UserService import UserService
from app.utils.enums import is_admin, enums
from app.models import User
import re

users_bp = Blueprint('users', __name__)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number (Pakistan format)"""
    if not phone:
        return True  # Phone is optional
    digits = re.sub(r'\D', '', phone)
    return len(digits) == 11

# GET all users (Admin only)
@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (Admin only)"""
    try:
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        users = UserService.get_all_users()
        return jsonify({
            'users': [user.to_dict() for user in users],
            'count': len(users)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET user by ID
@users_bp.route('/users/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID (Admin or own profile)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Users can view their own profile, admins can view any profile
        if current_user_id != user_id and not is_admin():
            return jsonify({'error': 'Access denied'}), 403
        
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST create user (Admin only)
@users_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """Create user (Admin only)"""
    try:
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'name', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate username
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', data['username']):
            return jsonify({'error': 'Username must be 3-20 alphanumeric characters'}), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate phone if provided
        if data.get('phone_number') and not validate_phone(data['phone_number']):
            return jsonify({'error': 'Invalid phone number format (11 digits required)'}), 400
        
        # Check if username or email already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create user
        new_user = UserService.create_user(data)
        return jsonify({
            'message': 'User created successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT update user
@users_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user (Admin or own profile)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        # Users can update their own profile, admins can update any profile
        if current_user_id != user_id and not is_admin():
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate phone if provided
        if data.get('phone_number') and not validate_phone(data['phone_number']):
            return jsonify({'error': 'Invalid phone number format (11 digits required)'}), 400
        
        # Check if email is already taken by another user
        if data.get('email'):
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({'error': 'Email already exists'}), 409
        
        # Non-admin users cannot change their role
        if data.get('role') is not None and current_user_id == user_id and current_user.role < enums.UserRole.isAdmin:
            return jsonify({'error': 'Cannot modify your own role'}), 403
        
        updated_user = UserService.update_user(user_id, data)
        if not updated_user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'User updated successfully',
            'user': updated_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE user (Admin only)
@users_bp.route('/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user (Admin only)"""
    try:
        current_user_id = get_jwt_identity()
        
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        # Prevent deleting own account
        if current_user_id == user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 403
        
        success = UserService.delete_user(user_id)
        if not success:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET current user profile
@users_bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user's profile"""
    try:
        current_user_id = get_jwt_identity()
        user = UserService.get_user_by_id(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT update current user profile
@users_bp.route('/users/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """Update current logged-in user's profile"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate phone if provided
        if data.get('phone_number') and not validate_phone(data['phone_number']):
            return jsonify({'error': 'Invalid phone number format (11 digits required)'}), 400
        
        # Check if email is already taken
        if data.get('email'):
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != current_user_id:
                return jsonify({'error': 'Email already exists'}), 409
        
        # Prevent role modification
        if 'role' in data:
            del data['role']
        
        updated_user = UserService.update_user(current_user_id, data)
        if not updated_user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': updated_user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
