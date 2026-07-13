from app.models import Book, Author, Category, db
from app.repositories.BookRepository import BookRepository
from datetime import datetime, timezone
from sqlalchemy import or_, and_

class BookService:
    """Service layer for Book operations"""
    
    @staticmethod
    def get_all_books(filters=None, search=None, include_details=False):
        """Get all active books with optional filters and search"""
        try:
            query = Book.query.filter_by(is_deleted=False)
            
            # Apply filters
            if filters:
                if filters.get('category_id'):
                    query = query.filter_by(category_id=filters['category_id'])
                if filters.get('author_id'):
                    query = query.filter_by(author_id=filters['author_id'])
                if filters.get('min_price'):
                    query = query.filter(Book.price >= filters['min_price'])
                if filters.get('max_price'):
                    query = query.filter(Book.price <= filters['max_price'])
                if filters.get('in_stock'):
                    query = query.filter(Book.stock_quantity > 0)
            
            # Apply search
            if search:
                search_term = f"%{search}%"
                query = query.filter(
                    or_(
                        Book.title.ilike(search_term),
                        Book.isbn.ilike(search_term),
                        Book.description.ilike(search_term)
                    )
                )
            
            books = query.all()
            
            # Convert to dict with optional details
            return [book.to_dict(include_author=include_details, include_category=include_details) for book in books]
        except Exception as e:
            raise e
    
    @staticmethod
    def get_book_by_id(book_id, include_details=True):
        """Get book by ID with optional author and category details"""
        book = Book.query.filter_by(id=book_id, is_deleted=False).first()
        if book:
            return book.to_dict(include_author=include_details, include_category=include_details)
        return None
    
    @staticmethod
    def create_book(data, created_by=None):
        """Create new book - Admin only"""
        try:
            # Validate required fields
            if not data.get('title'):
                raise ValueError('Title is required')
            if not data.get('price'):
                raise ValueError('Price is required')
            
            # Validate price is positive
            price = float(data['price'])
            if price <= 0:
                raise ValueError('Price must be greater than 0')
            
            # Check if ISBN already exists
            if data.get('isbn'):
                existing_book = Book.query.filter_by(isbn=data['isbn'], is_deleted=False).first()
                if existing_book:
                    raise ValueError('A book with this ISBN already exists')
            
            # Validate author if provided
            if data.get('author_id'):
                author = Author.query.filter_by(id=data['author_id'], is_deleted=False).first()
                if not author:
                    raise ValueError('Author not found')
            
            # Validate category if provided
            if data.get('category_id'):
                category = Category.query.filter_by(id=data['category_id'], is_deleted=False).first()
                if not category:
                    raise ValueError('Category not found')
            
            new_book = Book(
                title=data['title'],
                isbn=data.get('isbn'),
                price=price,
                stock_quantity=int(data.get('stock_quantity', 0)),
                description=data.get('description'),
                image_url=data.get('image_url'),
                author_id=data.get('author_id'),
                category_id=data.get('category_id'),
                created_by=created_by or ''
            )
            
            db.session.add(new_book)
            db.session.commit()
            return new_book.to_dict(include_author=True, include_category=True)
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_book(book_id, data):
        """Update existing book"""
        try:
            book = Book.query.filter_by(id=book_id, is_deleted=False).first()
            if not book:
                return None
            
            # Update fields if provided
            if 'title' in data:
                book.title = data['title']
            
            if 'isbn' in data and data['isbn'] != book.isbn:
                # Check if new ISBN already exists
                existing_book = Book.query.filter_by(isbn=data['isbn'], is_deleted=False).first()
                if existing_book and existing_book.id != book_id:
                    raise ValueError('A book with this ISBN already exists')
                book.isbn = data['isbn']
            
            if 'price' in data:
                price = float(data['price'])
                if price <= 0:
                    raise ValueError('Price must be greater than 0')
                book.price = price
            
            if 'stock_quantity' in data:
                book.stock_quantity = int(data['stock_quantity'])
            
            if 'description' in data:
                book.description = data['description']
            
            if 'image_url' in data:
                book.image_url = data['image_url']
            
            if 'author_id' in data:
                if data['author_id']:
                    author = Author.query.filter_by(id=data['author_id'], is_deleted=False).first()
                    if not author:
                        raise ValueError('Author not found')
                book.author_id = data['author_id']
            
            if 'category_id' in data:
                if data['category_id']:
                    category = Category.query.filter_by(id=data['category_id'], is_deleted=False).first()
                    if not category:
                        raise ValueError('Category not found')
                book.category_id = data['category_id']
            
            book.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return book.to_dict(include_author=True, include_category=True)
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def delete_book(book_id):
        """Soft delete book"""
        try:
            book = Book.query.filter_by(id=book_id, is_deleted=False).first()
            if not book:
                return False
            
            book.is_deleted = True
            book.deleted_at = datetime.now(timezone.utc)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def check_stock(book_id, quantity):
        """Check if sufficient stock is available"""
        book = Book.query.filter_by(id=book_id, is_deleted=False).first()
        if not book:
            return False
        return book.stock_quantity >= quantity
    
    @staticmethod
    def update_stock(book_id, quantity, operation='reduce'):
        """Update stock quantity (reduce or add)"""
        try:
            book = Book.query.filter_by(id=book_id, is_deleted=False).with_for_update().first()
            if not book:
                return False
            
            if operation == 'reduce':
                if book.stock_quantity < quantity:
                    return False
                book.stock_quantity -= quantity
            elif operation == 'add':
                book.stock_quantity += quantity
            else:
                return False
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def search_books(query_string):
        """Search books by title, ISBN, or description"""
        if not query_string:
            return []
        
        search_term = f"%{query_string}%"
        books = Book.query.filter(
            and_(
                Book.is_deleted == False,
                or_(
                    Book.title.ilike(search_term),
                    Book.isbn.ilike(search_term),
                    Book.description.ilike(search_term)
                )
            )
        ).all()
        
        return [book.to_dict(include_author=True, include_category=True) for book in books]
