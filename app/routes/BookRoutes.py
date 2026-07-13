from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.BookService import BookService
from app.utils.enums import is_admin

book_bp = Blueprint("books", __name__)

# GET all books (with optional filters and search)
@book_bp.route('/books', methods=['GET'])
def get_books():
    """Get all books with optional filters
    
    Query Parameters:
    - category_id: Filter by category
    - author_id: Filter by author
    - min_price: Minimum price (PKR)
    - max_price: Maximum price (PKR)
    - in_stock: Only show books in stock (true/false)
    - search: Search in title, ISBN, description
    - include_details: Include author and category details (true/false)
    """
    try:
        # Get query parameters
        filters = {}
        if request.args.get('category_id'):
            filters['category_id'] = request.args.get('category_id')
        if request.args.get('author_id'):
            filters['author_id'] = request.args.get('author_id')
        if request.args.get('min_price'):
            try:
                filters['min_price'] = float(request.args.get('min_price'))
            except ValueError:
                return jsonify({'error': 'Invalid min_price format'}), 400
        if request.args.get('max_price'):
            try:
                filters['max_price'] = float(request.args.get('max_price'))
            except ValueError:
                return jsonify({'error': 'Invalid max_price format'}), 400
        if request.args.get('in_stock'):
            filters['in_stock'] = request.args.get('in_stock').lower() == 'true'
        
        search = request.args.get('search')
        include_details = request.args.get('include_details', 'true').lower() == 'true'
        
        books = BookService.get_all_books(
            filters=filters if filters else None,
            search=search,
            include_details=include_details
        )
        
        return jsonify({
            'books': books,
            'count': len(books)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET book by ID
@book_bp.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    """Get book by ID with full details"""
    try:
        book = BookService.get_book_by_id(book_id, include_details=True)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({'book': book}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GET search books
@book_bp.route('/books/search', methods=['GET'])
def search_books():
    """Search books by title, ISBN, or description
    
    Query Parameters:
    - q: Search query string (required)
    """
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({'error': 'Search query (q) is required'}), 400
        
        books = BookService.search_books(query)
        
        return jsonify({
            'books': books,
            'count': len(books),
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# POST create book (Admin only)
@book_bp.route('/books', methods=['POST'])
@jwt_required()
def create_book():
    """Create new book (Admin only)
    
    Required fields:
    - title: Book title
    - price: Price in PKR (must be > 0)
    
    Optional fields:
    - isbn: ISBN number
    - stock_quantity: Available stock (default: 0)
    - description: Book description
    - image_url: URL to book cover image
    - author_id: Author ID
    - category_id: Category ID
    """
    try:
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        current_user_id = get_jwt_identity()
        
        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400
        if not data.get('price'):
            return jsonify({'error': 'Price is required'}), 400
        
        # Validate price
        try:
            price = float(data['price'])
            if price <= 0:
                return jsonify({'error': 'Price must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid price format'}), 400
        
        book = BookService.create_book(data, created_by=current_user_id)
        
        return jsonify({
            'message': 'Book created successfully',
            'book': book
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT update book (Admin only)
@book_bp.route('/books/<book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    """Update book (Admin only)
    
    Optional fields to update:
    - title: Book title
    - isbn: ISBN number
    - price: Price in PKR
    - stock_quantity: Available stock
    - description: Book description
    - image_url: URL to book cover image
    - author_id: Author ID
    - category_id: Category ID
    """
    try:
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate price if provided
        if 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    return jsonify({'error': 'Price must be greater than 0'}), 400
            except (ValueError, TypeError):
                return jsonify({'error': 'Invalid price format'}), 400
        
        book = BookService.update_book(book_id, data)
        
        if not book:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({
            'message': 'Book updated successfully',
            'book': book
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE book (Admin only)
@book_bp.route('/books/<book_id>', methods=['DELETE'])
@jwt_required()
def delete_book(book_id):
    """Delete book (Admin only) - Soft delete"""
    try:
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        success = BookService.delete_book(book_id)
        
        if not success:
            return jsonify({'error': 'Book not found'}), 404
        
        return jsonify({'message': 'Book deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# PUT update stock (Admin only)
@book_bp.route('/books/<book_id>/stock', methods=['PUT'])
@jwt_required()
def update_stock(book_id):
    """Update book stock (Admin only)
    
    Request body:
    - quantity: Amount to add or reduce
    - operation: 'add' or 'reduce' (default: 'add')
    """
    try:
        # Check if user is admin
        if not is_admin():
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        if 'quantity' not in data:
            return jsonify({'error': 'Quantity is required'}), 400
        
        try:
            quantity = int(data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid quantity format'}), 400
        
        operation = data.get('operation', 'add')
        if operation not in ['add', 'reduce']:
            return jsonify({'error': 'Operation must be "add" or "reduce"'}), 400
        
        success = BookService.update_stock(book_id, quantity, operation)
        
        if not success:
            if operation == 'reduce':
                return jsonify({'error': 'Insufficient stock or book not found'}), 400
            return jsonify({'error': 'Book not found'}), 404
        
        # Get updated book
        book = BookService.get_book_by_id(book_id)
        
        return jsonify({
            'message': 'Stock updated successfully',
            'book': book
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
