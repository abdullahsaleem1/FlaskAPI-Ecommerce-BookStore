import os
from app import create_app
from app.models import db

# ---------------------------------------------------------------------------
# Vercel requires a top-level "app" variable to be present in this file.
# We always create it here; the correct config is selected via env-vars.
# ---------------------------------------------------------------------------
if os.environ.get('VERCEL') or os.environ.get('FLASK_ENV') == 'production':
    from config.production import ProductionConfig
    app = create_app(ProductionConfig)
else:
    app = create_app()

# Expose as "application" as well (some WSGI servers look for this name)
application = app

# Create database tables
# Comment this out when using Flask-Migrate
# with app.app_context():
#     db.create_all()
#     print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
