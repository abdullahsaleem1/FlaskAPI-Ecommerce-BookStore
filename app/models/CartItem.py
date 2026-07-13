from app.models import db
from app.models.BaseModel import BaseModel

class CartItem(BaseModel, db.Model):
    __tablename__ = 'cart_items'
    
    # CartItem fields
    quantity = db.Column(db.Integer, nullable=False, default=1)
    
    # Foreign Keys
    book_id = db.Column(db.String(36), db.ForeignKey('books.id'), nullable=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    book = db.relationship('Book', backref='cart_items', lazy=True)
    user = db.relationship('User', backref='cart_items', lazy=True)
    
    def to_dict(self, include_book=False, include_user=False):
        """Convert cart item to dictionary"""
        
        result = {
            **self.base_to_dict(),
            'quantity': self.quantity,
            'book_id': self.book_id,
            'user_id': self.user_id,
        }
        
        if include_book and self.book:
            result['book'] = self.book.to_dict()
            result['subtotal'] = float(self.book.price) * self.quantity if self.book.price else 0
        
        if include_user and self.user:
            result['user'] = {
                'id': self.user.id,
                'username': self.user.username,
                'name': self.user.name,
                'email': self.user.email
            }
        
        return result
