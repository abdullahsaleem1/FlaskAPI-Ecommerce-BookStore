from datetime import datetime, timezone
from app.models import db
import uuid

class BaseModel:
    """Base model mixin with common fields for all models"""
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.String(255), nullable=True, default='')
    role = db.Column(db.Integer, nullable=False, default=0)  # 0=User, 1=Admin
    is_active = db.Column(db.Integer, nullable=False, default=1)  # 1=Active, 0=Inactive
    
    def base_to_dict(self):
        """Returns base fields as dictionary"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at.isoformat() if self.deleted_at else None,
            'created_by': self.created_by,
            'role': self.role,
            'is_active': self.is_active,
        }
