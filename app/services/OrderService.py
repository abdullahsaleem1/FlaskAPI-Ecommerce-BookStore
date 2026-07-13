from app.repositories.OrderDetailsRepository import OrderDetailsRepository
from app.repositories.OrderItemRepository import OrderItemRepository
from app.repositories.CartItemRepository import CartItemRepository
from app.repositories.BookRepository import BookRepository
from app.models import db, Book, CartItem
from typing import List, Dict, Optional
from datetime import datetime, timezone

class OrderService:
    """Service layer for Order business logic"""
    
    def __init__(self):
        self.order_repository = OrderDetailsRepository()
        self.order_item_repository = OrderItemRepository()
        self.cart_repository = CartItemRepository()
        self.book_repository = BookRepository()
    
    def create_order_from_cart(self, user_id: str, shipping_data: dict) -> Dict:
        """Create order from user's cart (checkout process with transaction)"""
        try:
            # Get cart items
            cart_items = self.cart_repository.get_by_user_id(user_id)
            
            if not cart_items:
                raise ValueError('Cart is empty')
            
            # Calculate total and validate stock
            total_amount = 0
            for cart_item in cart_items:
                book = self.book_repository.get_by_id(cart_item.book_id)
                if not book:
                    raise ValueError(f'Book not found')
                
                if book.stock_quantity < cart_item.quantity:
                    raise ValueError(f'Insufficient stock for {book.title}. Available: {book.stock_quantity}')
                
                total_amount += float(book.price) * cart_item.quantity
            
            # Create order
            order_data = {
                'user_id': user_id,
                'total_amount': total_amount,
                'order_status': 'Pending',
                'shipping_address': shipping_data.get('shipping_address', ''),
                'city': shipping_data.get('city', ''),
                'phone_number': shipping_data.get('phone_number', ''),
                'payment_method': shipping_data.get('payment_method', 'Cash on Delivery'),
                'notes': shipping_data.get('notes')
            }
            
            order = self.order_repository.create(order_data)
            
            # Create order items and reduce stock
            order_items_data = []
            for cart_item in cart_items:
                # Lock book row and reduce stock
                book = Book.query.with_for_update().get(cart_item.book_id)
                
                if book.stock_quantity < cart_item.quantity:
                    db.session.rollback()
                    raise ValueError(f'Stock changed for {book.title}')
                
                book.stock_quantity -= cart_item.quantity
                
                # Prepare order item data
                order_items_data.append({
                    'order_details_id': order.id,
                    'book_id': cart_item.book_id,
                    'user_id': user_id,
                    'unit_price': book.price,
                    'quantity': cart_item.quantity
                })
                
                # Soft delete cart item
                self.cart_repository.delete(cart_item)
            
            # Create all order items
            self.order_item_repository.create_batch(order_items_data)
            
            db.session.commit()
            
            # Return order with items
            return self.get_order_details(order.id, user_id)
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_user_orders(self, user_id: str) -> List[Dict]:
        """Get all orders for a user"""
        orders = self.order_repository.get_by_user_id(user_id)
        return [self._order_to_dict_summary(order) for order in orders]
    
    def get_recent_orders(self, user_id: str, limit: int = 5) -> List[Dict]:
        """Get recent orders for a user"""
        orders = self.order_repository.get_recent_orders(user_id, limit)
        return [self._order_to_dict_summary(order) for order in orders]
    
    def get_order_details(self, order_id: str, user_id: str = None) -> Optional[Dict]:
        """Get order by ID with full details"""
        order = self.order_repository.get_by_id(order_id)
        
        if not order:
            return None
        
        # Check permission
        if user_id and order.user_id != user_id:
            raise PermissionError('Unauthorized to view this order')
        
        # Get order items
        items = self.order_item_repository.get_by_order_id(order_id)
        
        order_dict = order.to_dict()
        order_dict['items'] = [item.to_dict() for item in items]
        order_dict['item_count'] = order.item_count
        
        return order_dict
    
    def get_all_orders(self) -> List[Dict]:
        """Get all orders (Admin only)"""
        orders = self.order_repository.get_all()
        return [self._order_to_dict_summary(order) for order in orders]
    
    def get_orders_by_status(self, status: str) -> List[Dict]:
        """Get orders by status (Admin only)"""
        orders = self.order_repository.get_by_status(status)
        return [self._order_to_dict_summary(order) for order in orders]
    
    def update_order_status(self, order_id: str, status: str) -> Optional[Dict]:
        """Update order status (Admin only)"""
        valid_statuses = ['Pending', 'Confirmed', 'Shipped', 'Delivered', 'Cancelled']
        
        if status not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        
        # Check if status transition is valid
        if not order.can_update_status(status):
            raise ValueError(f'Cannot change status from {order.order_status} to {status}')
        
        update_data = {'order_status': status}
        updated_order = self.order_repository.update(order, update_data)
        
        return self.get_order_details(updated_order.id)
    
    def update_tracking_number(self, order_id: str, tracking_number: str) -> Optional[Dict]:
        """Update order tracking number (Admin only)"""
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return None
        
        update_data = {'tracking_number': tracking_number}
        updated_order = self.order_repository.update(order, update_data)
        
        return updated_order.to_dict()
    
    def cancel_order(self, order_id: str, user_id: str, is_admin: bool = False) -> Dict:
        """Cancel an order and restore stock"""
        order = self.order_repository.get_by_id(order_id)
        
        if not order:
            raise ValueError('Order not found')
        
        # Check permissions
        if not is_admin and order.user_id != user_id:
            raise PermissionError('Unauthorized to cancel this order')
        
        # Check if order can be cancelled
        if not order.can_cancel():
            raise ValueError(f'Cannot cancel order with status: {order.order_status}')
        
        try:
            # Restore stock for all items
            order_items = self.order_item_repository.get_by_order_id(order_id)
            
            for item in order_items:
                book = Book.query.with_for_update().get(item.book_id)
                if book:
                    book.stock_quantity += item.quantity
            
            # Update order status
            update_data = {'order_status': 'Cancelled'}
            updated_order = self.order_repository.update(order, update_data)
            
            db.session.commit()
            
            return self.get_order_details(updated_order.id)
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    def _order_to_dict_summary(self, order) -> Dict:
        """Convert order to dict with summary info"""
        order_dict = order.to_dict()
        order_dict['item_count'] = order.item_count
        # Add user name for admin dashboard
        if order.user:
            order_dict['user_name'] = order.user.name
        return order_dict
