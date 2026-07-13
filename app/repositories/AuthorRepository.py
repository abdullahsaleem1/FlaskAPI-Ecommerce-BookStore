from app.models import Author, db
from typing import List, Optional, Dict
from datetime import datetime, timezone
from app.utils import enums

class AuthorRepository:
    """Repository for Author database operations"""
    
    def create(self, author_data: dict) -> Author:
        """Create a new author"""
        author = Author(**author_data)
        db.session.add(author)
        db.session.flush()
        return author
    
    def get_by_id(self, author_id: str) -> Optional[Author]:
        """Get author by ID"""
        return Author.query.filter_by(id=author_id, is_deleted=False).first()
    
    def get_all_authors(self) -> List[Author]:
        """Get all authors"""
        return Author.query.filter_by(is_deleted=False).order_by(Author.author_name).all()
    
    def get_author_by_name(self, author_name: str) -> Optional[Author]:
        """Get author by exact name"""
        return Author.query.filter(
            Author.author_name.ilike(author_name),
            Author.is_deleted == False
        ).first()
    
    def search_by_name(self, name: str) -> List[Author]:
        """Search authors by name (partial match)"""
        return Author.query.filter(
            Author.author_name.ilike(f'%{name}%'),
            Author.is_deleted == False
        ).order_by(Author.author_name).all()
    
    def update(self, author: Author, update_data: dict) -> Author:
        """Update author"""
        # Prevent updating certain fields
        protected_fields = ['id', 'created_at']
        for field in protected_fields:
            update_data.pop(field, None)
        
        for key, value in update_data.items():
            setattr(author, key, value)
        
        author.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        db.session.commit()
        return author
    
    def has_books(self, author: Author) -> bool:
        """Check if author has associated books"""
        return len(author.books) > 0
    
    def delete_author(self, author: Author) -> None:
        """Soft delete author"""
        author.is_active = enums.UserStatus.isInactive
        author.is_deleted = True
        author.deleted_at = datetime.now(timezone.utc)
        db.session.flush()
