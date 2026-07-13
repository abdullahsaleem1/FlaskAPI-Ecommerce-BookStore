from datetime import date, datetime
from app.models import db
from app.models.BaseModel import BaseModel
import re

class User(BaseModel, db.Model):
    __tablename__ = 'users'
    
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    province = db.Column(db.String(100), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            **self.base_to_dict(),
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'address': self.address,
            'province': self.province,
            'city': self.city,
            'phone_number': self.phone_number,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'role': self.role,
            'is_active': self.is_active
        }

def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    return 11 <= len(digits) <= 11
