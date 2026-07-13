from app.models import db
from app.models.BaseModel import BaseModel

class Author(BaseModel, db.Model):
    __tablename__ = 'authors'
    
    author_name = db.Column(db.String(255), nullable=False)
    
    # Relationship with Books
    books = db.relationship('Book', backref='author', lazy=True)
    
    def to_dict(self):
        return {
            **self.base_to_dict(),
            'author_name': self.author_name,
        }
