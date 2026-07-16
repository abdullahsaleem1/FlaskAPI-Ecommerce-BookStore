import os
from app import create_app
from app.models import db

# Use ProductionConfig on Vercel / any production environment
if os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production':
    from config.production import ProductionConfig
    app = create_app(ProductionConfig)
else:
    app = create_app()

# Create database tables
# Comment this out when using Flask-Migrate
# with app.app_context():
#     db.create_all()
#     print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
