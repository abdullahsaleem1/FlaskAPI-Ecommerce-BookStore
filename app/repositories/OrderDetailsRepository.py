from app.models import db
from app.models.OrderDetails import OrderDetails
from typing import List, Optional
from datetime import datetime, timezone

class OrderDetailsRepository:
    """Repository for OrderDetails database operations"""
    
    @staticmethod
    def create(order_data: dict) -> OrderDetails:
        """Create a new order"""
        order = OrderDetails(**order_data)
        db.session.add(order)
        db.session.commit()
        return order
    
    @staticmethod
    def get_by_id(order_id: str) -> Optional[OrderDetails]:
        """Get order by ID"""
        return OrderDetails.query.filter_by(id=order_id, is_deleted=False).first()
    
    @staticmethod
    def get_all() -> List[OrderDetails]:
        """Get all orders"""
        return OrderDetails.query.filter_by(is_deleted=False).order_by(OrderDetails.order_date.desc()).all()
    
    @staticmethod
    def get_by_user_id(user_id: str) -> List[OrderDetails]:
        """Get all orders for a specific user"""
        return OrderDetails.query.filter_by(
            user_id=user_id, 
            is_deleted=False
        ).order_by(OrderDetails.order_date.desc()).all()
    
    @staticmethod
    def get_by_status(status: str) -> List[OrderDetails]:
        """Get all orders by status"""
        return OrderDetails.query.filter_by(
            order_status=status, 
            is_deleted=False
        ).order_by(OrderDetails.order_date.desc()).all()
    
    @staticmethod
    def get_recent_orders(user_id: str, limit: int = 5) -> List[OrderDetails]:
        """Get recent orders for a user"""
        return OrderDetails.query.filter_by(
            user_id=user_id, 
            is_deleted=False
        ).order_by(OrderDetails.order_date.desc()).limit(limit).all()
    
    @staticmethod
    def update(order: OrderDetails, update_data: dict) -> OrderDetails:
        """Update order"""
        for key, value in update_data.items():
            if hasattr(order, key) and key not in ['id', 'user_id', 'order_date']:
                setattr(order, key, value)
        order.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return order
    
    @staticmethod
    def delete(order: OrderDetails) -> None:
        """Soft delete order"""
        order.is_deleted = True
        order.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
