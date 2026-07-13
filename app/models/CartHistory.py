from app.models import db
from app.models.BaseModel import BaseModel

class CartHistory(BaseModel, db.Model):
    __tablename__ = 'cart_history'
    
    # CartHistory fields
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Numeric(18, 2), nullable=False)
    
    # Foreign Keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    book_id = db.Column(db.String(36), db.ForeignKey('books.id'), nullable=True)
    order_item_id = db.Column(db.String(36), db.ForeignKey('order_items.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='cart_histories', lazy=True)
    book = db.relationship('Book', backref='cart_histories', lazy=True)
    order_item = db.relationship('OrderItem', backref='cart_histories', lazy=True)
    
    def to_dict(self):
        return {
            **self.base_to_dict(),
            'quantity': self.quantity,
            'price_at_purchase': float(self.price_at_purchase),
            'user_id': self.user_id,
            'book_id': self.book_id,
            'order_item_id': self.order_item_id,
        }
