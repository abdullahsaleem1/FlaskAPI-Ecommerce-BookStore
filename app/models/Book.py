from app.models import db
from app.models.BaseModel import BaseModel

# Book model for bookstore catalog
class Book(BaseModel, db.Model):
    __tablename__ = 'books'
    
    # Book-specific fields
    title = db.Column(db.String(255), nullable=False)
    isbn = db.Column(db.String(50), unique=True, nullable=True)
    price = db.Column(db.Numeric(18, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    
    # Foreign Keys
    author_id = db.Column(db.String(36), db.ForeignKey('authors.id'), nullable=True)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=True)
    
    # Relationships (backrefs defined in Author and Category models)
    # author = db.relationship('Author', backref='books', lazy=True)
    # category = db.relationship('Category', backref='books', lazy=True)
    
    def to_dict(self, include_author=False, include_category=False):
        """Convert book to dictionary
        
        Args:
            include_author: Include full author details
            include_category: Include full category details
        """
        result = {
            **self.base_to_dict(),
            'title': self.title,
            'isbn': self.isbn,
            'price': float(self.price) if self.price else None,
            'price_pkr': f"PKR {float(self.price):,.2f}" if self.price else None,
            'stock_quantity': self.stock_quantity,
            'description': self.description,
            'image_url': self.image_url,
            'author_id': self.author_id,
            'category_id': self.category_id,
            'in_stock': self.stock_quantity > 0
        }
        
        # Include author details if requested
        if include_author and self.author:
            result['author'] = {
                'id': self.author.id,
                'name': self.author.author_name
            }
        
        # Include category details if requested
        if include_category and self.category:
            result['category'] = {
                'id': self.category.id,
                'name': self.category.category_type
            }
        
        return result
