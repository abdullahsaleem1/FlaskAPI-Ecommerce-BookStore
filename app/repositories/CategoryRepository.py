from app.models import Category, db
from typing import List, Optional, Dict
from datetime import datetime, timezone

class CategoryRepository:
    """Repository for Category database operations"""
    
    def create(self, category_data: dict) -> Category:
        """Create a new category"""
        category = Category(**category_data)
        db.session.add(category)
        db.session.flush()
        return category
    
    def get_by_id(self, category_id: str) -> Optional[Category]:
        """Get category by ID"""
        return Category.query.filter_by(id=category_id, is_deleted=False).first()
    
    def get_all(self) -> List[Category]:
        """Get all categories"""
        return Category.query.filter_by(is_deleted=False).order_by(Category.category_type).all()
    
    def get_by_type(self, category_type: str) -> Optional[Category]:
        """Get category by exact type"""
        return Category.query.filter_by(category_type=category_type, is_deleted=False).first()
    
    def search_by_type(self, type_name: str) -> List[Category]:
        """Search categories by type (partial match)"""
        return Category.query.filter(
            Category.category_type.ilike(f'%{type_name}%'),
            Category.is_deleted == False
        ).order_by(Category.category_type).all()
    
    def update(self, category: Category, update_data: dict) -> Category:
        """Update category"""
        # Prevent updating certain fields
        protected_fields = ['id', 'created_at']
        for field in protected_fields:
            update_data.pop(field, None)
        
        for key, value in update_data.items():
            setattr(category, key, value)
        
        category.updated_at = datetime.now(timezone.utc)
        db.session.flush()
        return category
    
    def delete(self, category: Category) -> None:
        """Soft delete category"""
        category.is_deleted = True
        category.deleted_at = datetime.now(timezone.utc)
        db.session.flush()
