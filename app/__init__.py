from flask import Flask, send_from_directory
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config.development import DevelopmentConfig
from app.models import db
import os

jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    
    # Enable CORS for frontend
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', 
                                     'http://localhost:5000,http://127.0.0.1:5000,http://localhost:8000,http://127.0.0.1:8000,http://localhost:5500,http://127.0.0.1:5500,https://daastan.onrender.com')
    
    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins.split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Register blueprints with API versioning
    from app.routes.itemRoutes import items_bp
    from app.routes.UserRoutes import users_bp
    from app.routes.AuthRoutes import auth_bp
    from app.routes.AuthorRoutes import author_bp
    from app.routes.CategoryRoutes import category_bp
    from app.routes.BookRoutes import book_bp
    from app.routes.CartRoutes import cart_bp
    from app.routes.CartHistoryRoutes import cart_history_bp
    from app.routes.OrderRoutes import order_bp
    from app.routes.ReviewRoutes import review_bp
    
    # API v1 routes
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users_bp, url_prefix='/api/v1')
    app.register_blueprint(author_bp, url_prefix='/api/v1')
    app.register_blueprint(category_bp, url_prefix='/api/v1')
    app.register_blueprint(book_bp, url_prefix='/api/v1')
    app.register_blueprint(cart_bp, url_prefix='/api/v1')
    app.register_blueprint(cart_history_bp, url_prefix='/api/v1/cart-history')
    app.register_blueprint(order_bp, url_prefix='/api/v1')
    app.register_blueprint(review_bp, url_prefix='/api/v1/reviews')
    
    # Legacy routes (keep for backward compatibility)
    app.register_blueprint(items_bp, url_prefix='/api')
    
    # Serve frontend static files
    @app.route('/')
    def home():
        frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
        return send_from_directory(frontend_dir, 'index.html')
    
    @app.route('/favicon.ico')
    def favicon():
        frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
        return send_from_directory(frontend_dir, 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    
    @app.route('/<path:filename>')
    def serve_frontend(filename):
        # Only serve if it's not an API route
        if not filename.startswith('api/'):
            frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
            file_path = os.path.join(frontend_dir, filename)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                return send_from_directory(frontend_dir, filename)
            # If file doesn't exist and no extension, try HTML
            if '.' not in filename or filename.endswith('.html'):
                html_path = os.path.join(frontend_dir, filename if filename.endswith('.html') else f'{filename}.html')
                if os.path.exists(html_path):
                    return send_from_directory(frontend_dir, os.path.basename(html_path))
        return {"error": "File not found"}, 404
    
    return app
