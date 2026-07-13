from app.models import db
from app.models.Review import Review
from typing import List, Optional
from datetime import datetime, timezone

class ReviewRepository:
    """Repository for Review database operations"""
    
    @staticmethod
    def create(review_data: dict) -> Review:
        """Create a new review"""
        review = Review(**review_data)
        db.session.add(review)
        db.session.flush()
        return review
    
    @staticmethod
    def get_by_id(review_id: str) -> Optional[Review]:
        """Get review by ID"""
        return Review.query.filter_by(id=review_id, is_deleted=False).first()
    
    @staticmethod
    def get_all() -> List[Review]:
        """Get all reviews"""
        return Review.query.filter_by(is_deleted=False).all()
    
    @staticmethod
    def get_by_book_id(book_id: str) -> List[Review]:
        """Get all reviews for a specific book"""
        return Review.query.filter_by(book_id=book_id, is_deleted=False).all()
    
    @staticmethod
    def get_by_user_id(user_id: str) -> List[Review]:
        """Get all reviews by a specific user"""
        return Review.query.filter_by(user_id=user_id, is_deleted=False).all()
    
    @staticmethod
    def get_by_user_and_book(user_id: str, book_id: str) -> Optional[Review]:
        """Check if user already reviewed a book"""
        return Review.query.filter_by(
            user_id=user_id, 
            book_id=book_id, 
            is_deleted=False
        ).first()
    
    @staticmethod
    def update(review: Review, update_data: dict) -> Review:
        """Update review"""
        for key, value in update_data.items():
            if hasattr(review, key) and key not in ['id', 'user_id', 'book_id']:
                setattr(review, key, value)
        review.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        return review
    
    @staticmethod
    def delete(review: Review) -> None:
        """Soft delete review"""
        review.is_deleted = True
        review.deleted_at = datetime.now(timezone.utc)
        db.session.flush()
