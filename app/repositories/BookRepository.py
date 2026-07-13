from app.models import Book, db
from typing import List, Optional, Dict
from datetime import datetime, timezone

class BookRepository:
    """Repository for Book database operations"""
    
    def create(self, book_data: dict) -> Book:
        """Create a new book"""
        book = Book(**book_data)
        db.session.add(book)
        db.session.flush()
        return book
    
    def get_by_id(self, book_id: str) -> Optional[Book]:
        """Get book by ID"""
        return Book.query.filter_by(id=book_id, is_deleted=False).first()
    
    def get_all(self) -> List[Book]:
        """Get all books"""
        return Book.query.filter_by(is_deleted=False).all()
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        """Get book by ISBN"""
        return Book.query.filter_by(isbn=isbn, is_deleted=False).first()
    
    def get_by_category_id(self, category_id: str) -> List[Book]:
        """Get all books in a category"""
        return Book.query.filter_by(category_id=category_id, is_deleted=False).all()
    
    def get_by_author_id(self, author_id: str) -> List[Book]:
        """Get all books by an author"""
        return Book.query.filter_by(author_id=author_id, is_deleted=False).all()
    
    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title (partial match)"""
        return Book.query.filter(
            Book.title.ilike(f'%{title}%'),
            Book.is_deleted == False
        ).all()
    
    def get_in_stock(self) -> List[Book]:
        """Get all books that are in stock"""
        return Book.query.filter(
            Book.stock_quantity > 0,
            Book.is_deleted == False
        ).all()
    
    def update(self, book: Book, update_data: dict) -> Book:
        """Update book"""
        # Prevent updating certain fields
        protected_fields = ['id', 'created_at']
        for field in protected_fields:
            update_data.pop(field, None)
        
        for key, value in update_data.items():
            setattr(book, key, value)
        
        book.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        return book
    
    def delete(self, book: Book) -> None:
        """Soft delete book"""
        book.is_deleted = True
        book.deleted_at = datetime.now(timezone.utc)
        db.session.flush()
    
    def reduce_stock(self, book: Book, quantity: int) -> Book:
        """Reduce book stock quantity"""
        if book.stock_quantity < quantity:
            raise ValueError(f'Insufficient stock for {book.title}')
        
        book.stock_quantity -= quantity
        book.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        return book
    
    def increase_stock(self, book: Book, quantity: int) -> Book:
        """Increase book stock quantity"""
        book.stock_quantity += quantity
        book.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        return book
