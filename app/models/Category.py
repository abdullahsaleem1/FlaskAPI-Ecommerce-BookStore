from app.models import db
from app.models.BaseModel import BaseModel

class Category(BaseModel, db.Model):
    __tablename__ = 'categories'
    
    category_type = db.Column(db.String(255), nullable=False)
    
    # Relationship with Books
    books = db.relationship('Book', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            **self.base_to_dict(),
            'category_type': self.category_type,
        }
