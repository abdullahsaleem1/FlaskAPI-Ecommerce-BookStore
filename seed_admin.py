"""
Seed script to create default admin user
Run this script once to create an admin account in the database
"""
from app import create_app
from app.models import db, User
from flask_bcrypt import Bcrypt
import uuid

def create_admin():
    app = create_app()
    bcrypt = Bcrypt(app)
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@bookstore.com').first()
        
        if existing_admin:
            print("[WARNING] Admin user already exists!")
            print(f"   Email: admin@bookstore.com")
            return
        
        # Create admin user
        admin = User(
            id=str(uuid.uuid4()),
            username='admin',
            name='System Administrator',
            email='admin@bookstore.com',
            password=bcrypt.generate_password_hash('Admin@123').decode('utf-8'),
            role=1,  # 1 = Admin
            is_active=1,
            address='Admin Office',
            city='Headquarters',
            province='N/A',
            phone_number='0000000000'
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("[INFO] Admin user created successfully!")
        print("=" * 50)
        print("Email:    admin@bookstore.com")
        print("Password: Admin@123")
        print("=" * 50)
        print("[WARNING] IMPORTANT: Change this password after first login!")

if __name__ == '__main__':
    create_admin()
