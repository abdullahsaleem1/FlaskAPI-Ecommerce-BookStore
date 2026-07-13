from flask_jwt_extended import get_jwt_identity
from app.models import User

class enums:
    class UserRole:
        isUser = 0
        isAdmin = 1
        
    class UserStatus:
        isInactive = 0
        isActive = 1

def is_admin():
    """Check if current user is admin (role >= 1)"""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return user and user.role >= 1


