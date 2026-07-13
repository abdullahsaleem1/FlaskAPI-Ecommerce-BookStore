from app.models import db
from app.models.BaseModel import BaseModel
from datetime import datetime, timezone

class OrderDetails(BaseModel, db.Model):
    __tablename__ = 'order_details'
    
    # OrderDetails fields
    total_amount = db.Column(db.Numeric(18, 2), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    order_status = db.Column(db.String(20), nullable=False, default='Pending')  # Pending, Confirmed, Shipped, Delivered, Cancelled
    shipping_address = db.Column(db.String(255), nullable=False, default='')
    city = db.Column(db.String(100), nullable=False, default='')
    phone_number = db.Column(db.String(15), nullable=False, default='')
    tracking_number = db.Column(db.String(100), nullable=True)
    payment_method = db.Column(db.String(50), nullable=True, default='Cash on Delivery')
    notes = db.Column(db.Text, nullable=True)
    
    # Foreign Key
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='orders', lazy=True)
    # Note: order_items relationship is defined via backref in OrderItem model
    
    @property
    def item_count(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.order_items if not item.is_deleted)
    
    def can_cancel(self):
        """Check if order can be cancelled"""
        return self.order_status in ['Pending', 'Confirmed']
    
    def can_update_status(self, new_status):
        """Check if status transition is valid"""
        valid_transitions = {
            'Pending': ['Confirmed', 'Cancelled'],
            'Confirmed': ['Shipped', 'Cancelled'],
            'Shipped': ['Delivered'],
            'Delivered': [],
            'Cancelled': []
        }
        return new_status in valid_transitions.get(self.order_status, [])
    
    def to_dict(self):
        return {
            **self.base_to_dict(),
            'total_amount': float(self.total_amount),
            'order_date': self.order_date.isoformat() if self.order_date else None,
            'order_status': self.order_status,
            'shipping_address': self.shipping_address,
            'city': self.city,
            'phone_number': self.phone_number,
            'tracking_number': self.tracking_number,
            'payment_method': self.payment_method,
            'notes': self.notes,
            'user_id': self.user_id,
            'item_count': self.item_count,
        }
