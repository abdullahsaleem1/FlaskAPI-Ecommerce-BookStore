"""
Seed script to create test users (admin + regular user)
Run this script once to populate the database with test accounts
"""
from app import create_app
from app.models import db
from flask_bcrypt import Bcrypt
import uuid
from datetime import datetime, timezone

def create_test_users():
    app = create_app()
    bcrypt = Bcrypt(app)
    
    with app.app_context():
        print("Creating test users...")
        print("=" * 60)
        
        # Check if admin already exists
        result = db.session.execute(db.text("SELECT id FROM users WHERE email = 'admin@bookstore.com' AND is_deleted = false"))
        existing_admin = result.fetchone()
        
        if not existing_admin:
            # Create admin user with raw SQL
            admin_id = str(uuid.uuid4())
            admin_password = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
            now = datetime.now(timezone.utc)
            
            db.session.execute(db.text("""
                INSERT INTO users (id, username, name, email, password, address, province, city, 
                                 phone_number, role, is_active, created_at, updated_at, is_deleted, created_by)
                VALUES (:id, :username, :name, :email, :password, :address, :province, :city,
                       :phone, :role, :is_active, :created_at, :updated_at, :is_deleted, :created_by)
            """), {
                'id': admin_id,
                'username': 'admin',
                'name': 'System Administrator',
                'email': 'admin@bookstore.com',
                'password': admin_password,
                'address': 'Admin Office',
                'province': 'N/A',
                'city': 'Headquarters',
                'phone': '0000000000',
                'role': 1,
                'is_active': 1,
                'created_at': now,
                'updated_at': now,
                'is_deleted': False,
                'created_by': ''
            })
            print("[INFO] Admin user created")
        else:
            print("[INFO] Admin already exists")
        
        result = db.session.execute(db.text("SELECT id FROM users WHERE email = 'user@bookstore.com' AND is_deleted = false"))
        existing_user = result.fetchone()
        
        if not existing_user:
            user_id = str(uuid.uuid4())
            user_password = bcrypt.generate_password_hash('User@123').decode('utf-8')
            now = datetime.now(timezone.utc)
            
            db.session.execute(db.text("""
                INSERT INTO users (id, username, name, email, password, address, province, city,
                                 phone_number, role, is_active, created_at, updated_at, is_deleted, created_by)
                VALUES (:id, :username, :name, :email, :password, :address, :province, :city,
                       :phone, :role, :is_active, :created_at, :updated_at, :is_deleted, :created_by)
            """), {
                'id': user_id,
                'username': 'testuser',
                'name': 'Test User',
                'email': 'user@bookstore.com',
                'password': user_password,
                'address': '123 Test Street',
                'province': 'Test Province',
                'city': 'Test City',
                'phone': '1234567890',
                'role': 0,
                'is_active': 1,
                'created_at': now,
                'updated_at': now,
                'is_deleted': False,
                'created_by': ''
            })
            print("[INFO] Test user created")
        else:
            print("[WARNING]  Test user already exists")
        
        db.session.commit()
        
        print("=" * 60)
        print(" TEST ACCOUNTS:")
        print("=" * 60)
        print("\n ADMIN ACCOUNT:")
        print("   Email:    admin@bookstore.com")
        print("   Password: Admin@123")
        print("   Role:     Administrator")
        print("\n REGULAR USER ACCOUNT:")
        print("   Email:    user@bookstore.com")
        print("   Password: User@123")
        print("   Role:     User")
        print("=" * 60)
        print("[WARNING]: Change these passwords in production!")
        print("\n You can now login in Postman using these credentials")

if __name__ == '__main__':
    create_test_users()
