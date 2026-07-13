from app.models import User, db
from datetime import datetime, timezone

class UserRepository:
    """Repository for User database operations"""
    
    @staticmethod
    def get_all(include_deleted=False):
        """Get all users"""
        if include_deleted:
            return User.query.all()
        return User.query.filter_by(deleted_at=None).all()
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        return User.query.filter_by(id=user_id, deleted_at=None).first()
    
    @staticmethod
    def get_by_username(username):
        """Get user by username"""
        return User.query.filter_by(username=username, deleted_at=None).first()
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        return User.query.filter_by(email=email, deleted_at=None).first()
    
    @staticmethod
    def create(user):
        """Create a new user"""
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update(user):
        """Update user"""
        user.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return user
    
    @staticmethod
    def delete(user_id):
        """Soft delete user"""
        user = User.query.filter_by(id=user_id, deleted_at=None).first()
        if user:
            user.deleted_at = datetime.now(timezone.utc)
            user.is_deleted = True
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def hard_delete(user_id):
        """Permanently delete user"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False
