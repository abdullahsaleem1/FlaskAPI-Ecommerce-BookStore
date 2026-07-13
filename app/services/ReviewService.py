from app.repositories.ReviewRepository import ReviewRepository
from app.repositories.BookRepository import BookRepository
from typing import List, Dict, Optional

class ReviewService:
    """Service layer for Review business logic"""
    
    def __init__(self):
        self.review_repository = ReviewRepository()
        self.book_repository = BookRepository()
    
    def create_review(self, user_id: str, book_id: str, rating: int, comment: str = None) -> Dict:
        """Create a new review"""
        # Validate rating
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        # Check if book exists
        book = self.book_repository.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        
        # Check if user already reviewed this book
        existing_review = self.review_repository.get_by_user_and_book(user_id, book_id)
        if existing_review:
            raise ValueError("You have already reviewed this book")
        
        review_data = {
            'user_id': user_id,
            'book_id': book_id,
            'rating': rating,
            'comment': comment
        }
        
        review = self.review_repository.create(review_data)
        from app.models import db
        db.session.commit()
        return review.to_dict()
    
    def get_review(self, review_id: str) -> Optional[Dict]:
        """Get review by ID"""
        review = self.review_repository.get_by_id(review_id)
        return review.to_dict() if review else None
    
    def get_all_reviews(self) -> List[Dict]:
        """Get all reviews"""
        reviews = self.review_repository.get_all()
        return [review.to_dict() for review in reviews]
    
    def get_book_reviews(self, book_id: str) -> List[Dict]:
        """Get all reviews for a book"""
        reviews = self.review_repository.get_by_book_id(book_id)
        return [review.to_dict() for review in reviews]
    
    def get_book_rating_summary(self, book_id: str) -> Dict:
        """Get rating summary for a book (average rating, total reviews, distribution)"""
        reviews = self.review_repository.get_by_book_id(book_id)
        
        if not reviews:
            return {
                'average_rating': 0,
                'total_reviews': 0,
                'rating_distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }
        
        total_reviews = len(reviews)
        average_rating = sum(r.rating for r in reviews) / total_reviews
        
        # Calculate rating distribution
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for review in reviews:
            distribution[review.rating] += 1
        
        return {
            'average_rating': round(average_rating, 2),
            'total_reviews': total_reviews,
            'rating_distribution': distribution
        }
    
    def get_user_reviews(self, user_id: str) -> List[Dict]:
        """Get all reviews by a user"""
        reviews = self.review_repository.get_by_user_id(user_id)
        return [review.to_dict() for review in reviews]
    
    def update_review(self, review_id: str, user_id: str, update_data: Dict) -> Optional[Dict]:
        """Update a review (user can only update their own review)"""
        review = self.review_repository.get_by_id(review_id)
        if not review:
            return None
        
        # Check ownership
        if review.user_id != user_id:
            raise PermissionError("You can only update your own reviews")
        
        # Validate rating if provided
        if 'rating' in update_data and not 1 <= update_data['rating'] <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        updated_review = self.review_repository.update(review, update_data)
        from app.models import db
        db.session.commit()
        return updated_review.to_dict()
    
    def delete_review(self, review_id: str, user_id: str, is_admin: bool = False) -> bool:
        """Delete a review (user can delete own review, admin can delete any)"""
        review = self.review_repository.get_by_id(review_id)
        if not review:
            return False
        
        # Check ownership (unless admin)
        if not is_admin and review.user_id != user_id:
            raise PermissionError("You can only delete your own reviews")
        
        self.review_repository.delete(review)
        from app.models import db
        db.session.commit()
        return True
