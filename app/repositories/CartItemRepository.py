from app.models import CartItem, db
from typing import List, Optional, Dict
from datetime import datetime, timezone

class CartItemRepository:
    """Repository for CartItem database operations"""
    
    def create(self, cart_item_data: dict) -> CartItem:
        """Create a new cart item"""
        cart_item = CartItem(**cart_item_data)
        db.session.add(cart_item)
        db.session.flush()
        return cart_item
    
    def get_by_id(self, cart_item_id: str) -> Optional[CartItem]:
        """Get cart item by ID"""
        return CartItem.query.filter_by(id=cart_item_id, is_deleted=False).first()
    
    def get_all(self) -> List[CartItem]:
        """Get all cart items"""
        return CartItem.query.filter_by(is_deleted=False).all()
    
    def get_by_user_id(self, user_id: str) -> List[CartItem]:
        """Get all cart items for a user"""
        return CartItem.query.filter_by(user_id=user_id, is_deleted=False).all()
    
    def get_by_user_and_book(self, user_id: str, book_id: str) -> Optional[CartItem]:
        """Get cart item by user and book (check for duplicates)"""
        return CartItem.query.filter_by(
            user_id=user_id,
            book_id=book_id,
            is_deleted=False
        ).first()
    
    def update(self, cart_item: CartItem, update_data: dict) -> CartItem:
        """Update cart item"""
        # Prevent updating certain fields
        protected_fields = ['id', 'user_id', 'created_at']
        for field in protected_fields:
            update_data.pop(field, None)
        
        for key, value in update_data.items():
            setattr(cart_item, key, value)
        
        cart_item.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        return cart_item
    
    def delete(self, cart_item: CartItem) -> None:
        """Soft delete cart item"""
        cart_item.is_deleted = True
        cart_item.deleted_at = datetime.now(timezone.utc)
        db.session.flush()
    
    def clear_user_cart(self, user_id: str) -> None:
        """Clear all cart items for a user (soft delete)"""
        cart_items = self.get_by_user_id(user_id)
        for item in cart_items:
            self.delete(item)
