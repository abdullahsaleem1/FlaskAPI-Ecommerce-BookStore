from flask import jsonify
from app.repositories.AuthorRepository import AuthorRepository
from app.models import db
from typing import List, Optional, Dict

class AuthorService:
    """Service layer for Author business logic"""
    
    def __init__(self):
        self.author_repository = AuthorRepository()
    
    def get_all_authors(self) -> List[Dict]:
        """Get all active authors"""
        authors = self.author_repository.get_all_authors()
        return [author.to_dict() for author in authors]
    
    def get_author_by_id(self, author_id: str) -> Optional[Dict]:
        """Get author by ID"""
        author = self.author_repository.get_by_id(author_id)
        return author.to_dict() if author else None
    
    def get_author_by_name(self, author_name: str) -> Optional[Dict]:
        """Get author by name"""
        if not author_name:
            return None
        author = self.author_repository.get_author_by_name(author_name)
        return author.to_dict() if author else None
    
    def search_authors(self, name: str) -> List[Dict]:
        """Search authors by name"""
        authors = self.author_repository.search_by_name(name)
        return [author.to_dict() for author in authors]
    
    def create_author(self, data: dict) -> Dict:
        """Create new author"""
        author_name = data.get('author_name')
        existing = self.author_repository.get_author_by_name(author_name)
        if existing:
            raise ValueError('Author with this name already exists')
        
        author_data = {
            'author_name': author_name,
            'created_by': data.get('created_by', '')
        }
        
        author = self.author_repository.create(author_data)
        db.session.commit()
        return author.to_dict()
    
    def update_author(self, author_name: str, data: dict) -> Optional[Dict]:
        """Update existing author"""
        author = self.author_repository.get_author_by_name(author_name)
        if not author:
            return None
        
        # Check if new name conflicts with existing author
        if 'author_name' in data and data['author_name'] != author.author_name:
            data['author_name'] = data['author_name']
            existing = self.author_repository.get_author_by_name(data['author_name'])
            if existing:
                raise ValueError('Author with this name already exists')
        
        update_data = {
            'author_name': data.get('author_name', author.author_name)
        }
        
        updated_author = self.author_repository.update(author, update_data)
        db.session.commit()
        return updated_author.to_dict()
    
    def delete_author(self, author_name: str) -> bool:
        """Soft delete author by name"""
        author = self.author_repository.get_author_by_name(author_name)
        
        if not author:
            return False
        
        if self.author_repository.has_books(author):
            raise ValueError('Cannot delete author with associated books')
        
        self.author_repository.delete_author(author)
        db.session.commit()
        return True
