from app.models import db
from app.models.OrderItem import OrderItem
from typing import List, Optional
from datetime import datetime, timezone

class OrderItemRepository:
    """Repository for OrderItem database operations"""
    
    @staticmethod
    def create(order_item_data: dict) -> OrderItem:
        """Create a new order item"""
        order_item = OrderItem(**order_item_data)
        db.session.add(order_item)
        db.session.commit()
        return order_item
    
    @staticmethod
    def create_batch(order_items_data: List[dict]) -> List[OrderItem]:
        """Create multiple order items at once"""
        order_items = [OrderItem(**item_data) for item_data in order_items_data]
        db.session.add_all(order_items)
        db.session.commit()
        return order_items
    
    @staticmethod
    def get_by_id(order_item_id: str) -> Optional[OrderItem]:
        """Get order item by ID"""
        return OrderItem.query.filter_by(id=order_item_id, is_deleted=False).first()
    
    @staticmethod
    def get_all() -> List[OrderItem]:
        """Get all order items"""
        return OrderItem.query.filter_by(is_deleted=False).all()
    
    @staticmethod
    def get_by_order_id(order_id: str) -> List[OrderItem]:
        """Get all items for a specific order"""
        return OrderItem.query.filter_by(
            order_details_id=order_id, 
            is_deleted=False
        ).all()
    
    @staticmethod
    def get_by_user_id(user_id: str) -> List[OrderItem]:
        """Get all order items for a specific user"""
        return OrderItem.query.filter_by(user_id=user_id, is_deleted=False).all()
    
    @staticmethod
    def update(order_item: OrderItem, update_data: dict) -> OrderItem:
        """Update order item"""
        for key, value in update_data.items():
            if hasattr(order_item, key) and key not in ['id', 'order_details_id', 'user_id']:
                setattr(order_item, key, value)
        order_item.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        return order_item
    
    @staticmethod
    def delete(order_item: OrderItem) -> None:
        """Soft delete order item"""
        order_item.is_deleted = True
        order_item.deleted_at = datetime.now(timezone.utc)
        db.session.commit()
