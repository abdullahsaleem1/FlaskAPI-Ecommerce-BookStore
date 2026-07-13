from app.models import User, db
from app.repositories.UserRepository import UserRepository
from app import bcrypt
from datetime import datetime, timezone
from app.utils.enums import enums

class UserService:
    """Service layer for User operations"""
    
    @staticmethod
    def get_all_users(include_deleted=False):
        """Get all users"""
        return UserRepository.get_all(include_deleted)
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        return UserRepository.get_by_id(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username"""
        return UserRepository.get_by_username(username)
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        return UserRepository.get_by_email(email)
    
    @staticmethod
    def create_user(data):
        """Create a new user"""
        try:
            # Hash password before storing
            hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            # Parse date_of_birth if provided
            date_of_birth = None
            if data.get('date_of_birth'):
                try:
                    date_of_birth = datetime.fromisoformat(data['date_of_birth'].replace('Z', '+00:00'))
                except:
                    pass
            
            new_user = User(
                username=data['username'],
                name=data['name'],
                email=data['email'],
                password=hashed_password,
                role=int(data.get('role', enums.UserRole.isUser)),
                phone_number=data.get('phone_number'),
                address=data.get('address'),
                city=data.get('city'),
                province=data.get('province'),
                date_of_birth=date_of_birth,
                is_active=int(data.get('is_active', enums.UserStatus.isActive))
            )
            
            return UserRepository.create(new_user)
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_user(user_id, data):
        """Update user"""
        try:
            user = UserRepository.get_by_id(user_id)
            if not user:
                return None
            
            # Update fields if provided
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                user.email = data['email']
            if 'phone_number' in data:
                user.phone_number = data['phone_number']
            if 'address' in data:
                user.address = data['address']
            if 'city' in data:
                user.city = data['city']
            if 'province' in data:
                user.province = data['province']
            if 'role' in data:
                user.role = int(data['role'])
            if 'is_active' in data:
                user.is_active = int(data['is_active'])
            if 'date_of_birth' in data and data['date_of_birth']:
                try:
                    user.date_of_birth = datetime.fromisoformat(data['date_of_birth'].replace('Z', '+00:00'))
                except:
                    pass
            
            # Update password if provided
            if 'password' in data and data['password']:
                user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
            
            return UserRepository.update(user)
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_user(user_id):
        """Soft delete user"""
        return UserRepository.delete(user_id)
    
    @staticmethod
    def activate_user(user_id):
        """Activate user"""
        user = UserRepository.get_by_id(user_id)
        if user:
            user.is_active = enums.UserStatus.isActive
            return UserRepository.update(user)
        return None
    
    @staticmethod
    def deactivate_user(user_id):
        """Deactivate user"""
        user = UserRepository.get_by_id(user_id)
        if user:
            user.is_active = enums.UserStatus.isInactive
            return UserRepository.update(user)
        return None
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None, "User not found"
        
        # Verify old password
        if not bcrypt.check_password_hash(user.password, old_password):
            return None, "Invalid old password"
        
        # Update password
        user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        return UserRepository.update(user), "Password changed successfully"
