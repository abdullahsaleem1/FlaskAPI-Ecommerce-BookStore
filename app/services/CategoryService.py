from app.repositories.CategoryRepository import CategoryRepository
from app.models import db
from typing import List, Optional, Dict

class CategoryService:
    """Service layer for Category business logic"""
    
    def __init__(self):
        self.category_repository = CategoryRepository()
    
    def get_all_categories(self) -> List[Dict]:
        """Get all active categories"""
        categories = self.category_repository.get_all()
        return [category.to_dict() for category in categories]
    
    def get_category_by_id(self, category_id: str) -> Optional[Dict]:
        """Get category by ID"""
        category = self.category_repository.get_by_id(category_id)
        return category.to_dict() if category else None
    
    def search_categories(self, type_name: str) -> List[Dict]:
        """Search categories by type"""
        categories = self.category_repository.search_by_type(type_name)
        return [category.to_dict() for category in categories]
    
    def create_category(self, data: dict) -> Dict:
        """Create new category"""
        # Check if category already exists
        existing = self.category_repository.get_by_type(data['category_type'])
        if existing:
            raise ValueError('Category with this type already exists')
        
        category_data = {
            'category_type': data['category_type'],
            'created_by': data.get('created_by', '')
        }
        
        category = self.category_repository.create(category_data)
        db.session.commit()
        return category.to_dict()
    
    def update_category(self, category_id: str, data: dict) -> Optional[Dict]:
        """Update existing category"""
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return None
        
        # Check if new type conflicts with existing category
        if 'category_type' in data and data['category_type'] != category.category_type:
            existing = self.category_repository.get_by_type(data['category_type'])
            if existing:
                raise ValueError('Category with this type already exists')
        
        update_data = {
            'category_type': data.get('category_type', category.category_type)
        }
        
        updated_category = self.category_repository.update(category, update_data)
        db.session.commit()
        return updated_category.to_dict()
    
    def delete_category(self, category_id: str) -> bool:
        """Soft delete category"""
        category = self.category_repository.get_by_id(category_id)
        if not category:
            return False
        
        self.category_repository.delete(category)
        db.session.commit()
        return True
