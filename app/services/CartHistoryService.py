from app.repositories.CartHistoryRepository import CartHistoryRepository
from typing import List, Dict, Optional

class CartHistoryService:
    """Service layer for CartHistory business logic"""
    
    def __init__(self):
        self.repository = CartHistoryRepository()
    
    def create_cart_history(self, user_id: str, book_id: str, order_item_id: str, 
                           quantity: int, price_at_purchase: float) -> Dict:
        """Create a new cart history record"""
        cart_history_data = {
            'user_id': user_id,
            'book_id': book_id,
            'order_item_id': order_item_id,
            'quantity': quantity,
            'price_at_purchase': price_at_purchase
        }
        
        cart_history = self.repository.create(cart_history_data)
        return cart_history.to_dict()
    
    def get_cart_history(self, cart_history_id: str) -> Optional[Dict]:
        """Get cart history by ID"""
        cart_history = self.repository.get_by_id(cart_history_id)
        return cart_history.to_dict() if cart_history else None
    
    def get_all_cart_history(self) -> List[Dict]:
        """Get all cart history records"""
        cart_histories = self.repository.get_all()
        return [ch.to_dict() for ch in cart_histories]
    
    def get_user_cart_history(self, user_id: str) -> List[Dict]:
        """Get cart history for a user"""
        cart_histories = self.repository.get_by_user_id(user_id)
        return [ch.to_dict() for ch in cart_histories]
    
    def get_order_item_history(self, order_item_id: str) -> List[Dict]:
        """Get cart history for an order item"""
        cart_histories = self.repository.get_by_order_item_id(order_item_id)
        return [ch.to_dict() for ch in cart_histories]
    
    def delete_cart_history(self, cart_history_id: str) -> bool:
        """Delete cart history"""
        cart_history = self.repository.get_by_id(cart_history_id)
        if not cart_history:
            return False
        
        self.repository.delete(cart_history)
        return True
