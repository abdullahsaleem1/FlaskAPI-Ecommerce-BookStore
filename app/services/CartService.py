from app.models import CartItem, Book, db
from app.repositories.CartItemRepository import CartItemRepository
from datetime import datetime, timezone

class CartService:
    """Service layer for Cart operations"""
    
    def __init__(self):
        self.cart_repo = CartItemRepository()
    
    @staticmethod
    def get_user_cart(user_id):
        """Get all cart items for a user with book details"""
        cart_items = CartItem.query.filter_by(user_id=user_id, is_deleted=False).all()
        result = []
        
        for item in cart_items:
            book = Book.query.filter_by(id=item.book_id, is_deleted=False).first()
            if book:
                item_dict = item.to_dict()
                item_dict['book'] = book.to_dict()
                item_dict['subtotal'] = float(book.price) * item.quantity
                result.append(item_dict)
        
        return result
    
    @staticmethod
    def get_cart_item_by_id(cart_item_id, user_id):
        """Get specific cart item for a user"""
        return CartItem.query.filter_by(
            id=cart_item_id,
            user_id=user_id,
            is_deleted=False
        ).first()
    
    @staticmethod
    def add_to_cart(user_id, book_id, quantity=1):
        """Add item to cart or update quantity if exists"""
        try:
            # Validate quantity
            if quantity <= 0:
                raise ValueError('Quantity must be greater than 0')
            
            # Check if book exists and has stock
            book = Book.query.filter_by(id=book_id, is_deleted=False).first()
            if not book:
                raise ValueError('Book not found')
            
            if book.is_active != 1:
                raise ValueError('Book is not available')
            
            if book.stock_quantity < quantity:
                raise ValueError(f'Insufficient stock. Available: {book.stock_quantity}')
            
            # Check if item already in cart
            cart_item = CartItem.query.filter_by(
                user_id=user_id, 
                book_id=book_id, 
                is_deleted=False
            ).first()
            
            if cart_item:
                # Update quantity
                new_quantity = cart_item.quantity + quantity
                if book.stock_quantity < new_quantity:
                    raise ValueError(f'Insufficient stock. Available: {book.stock_quantity}, current in cart: {cart_item.quantity}')
                cart_item.quantity = new_quantity
                cart_item.updated_at = datetime.now(timezone.utc)
            else:
                # Create new cart item
                cart_item = CartItem(
                    user_id=user_id,
                    book_id=book_id,
                    quantity=quantity
                )
                db.session.add(cart_item)
            
            db.session.commit()
            return cart_item
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_cart_item(cart_item_id, user_id, quantity):
        """Update cart item quantity"""
        try:
            # Validate quantity
            if quantity <= 0:
                raise ValueError('Quantity must be greater than 0')
            
            cart_item = CartItem.query.filter_by(
                id=cart_item_id, 
                user_id=user_id, 
                is_deleted=False
            ).first()
            
            if not cart_item:
                return None
            
            # Check stock
            book = Book.query.filter_by(id=cart_item.book_id, is_deleted=False).first()
            if not book:
                raise ValueError('Book not found')
            
            if book.stock_quantity < quantity:
                raise ValueError(f'Insufficient stock. Available: {book.stock_quantity}')
            
            cart_item.quantity = quantity
            cart_item.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return cart_item
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def remove_from_cart(cart_item_id, user_id):
        """Remove item from cart"""
        try:
            cart_item = CartItem.query.filter_by(
                id=cart_item_id, 
                user_id=user_id, 
                is_deleted=False
            ).first()
            
            if not cart_item:
                return False
            
            cart_item.is_deleted = True
            cart_item.deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def clear_cart(user_id):
        """Clear all items from user's cart"""
        try:
            cart_items = CartItem.query.filter_by(user_id=user_id, is_deleted=False).all()
            for item in cart_items:
                item.is_deleted = True
                item.deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_cart_summary(user_id):
        """Get cart summary with total, item count, etc."""
        cart_items = CartItem.query.filter_by(user_id=user_id, is_deleted=False).all()
        
        total = 0
        item_count = 0
        items = []
        
        for item in cart_items:
            book = Book.query.filter_by(id=item.book_id, is_deleted=False).first()
            if book:
                subtotal = float(book.price) * item.quantity
                total += subtotal
                item_count += item.quantity
                
                items.append({
                    'cart_item_id': item.id,
                    'book_id': book.id,
                    'title': book.title,
                    'price': float(book.price),
                    'quantity': item.quantity,
                    'subtotal': subtotal,
                    'stock_available': book.stock_quantity
                })
        
        return {
            'items': items,
            'total_items': len(items),
            'total_quantity': item_count,
            'total_price': total
        }
