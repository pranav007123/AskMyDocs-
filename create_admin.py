"""
Simple script to create an admin account or make existing user admin
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db, User

def create_or_make_admin():
    """Create admin account or promote existing user."""
    with app.app_context():
        print("=" * 60)
        print("Admin Account Setup")
        print("=" * 60)
        
        # Check if admin column exists, if not add it
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'is_admin' not in columns:
            print("Adding is_admin column to database...")
            try:
                db.session.execute(text(
                    "ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"
                ))
                db.session.commit()
                print("✅ Database updated successfully!")
            except Exception as e:
                print(f"Note: {e}")
                db.session.rollback()
        
        # List existing users
        users = User.query.all()
        
        if not users:
            print("\n❌ No users found in database.")
            print("Please register a user first at http://localhost:5000/register")
            print("Then run this script again.")
            return
        
        print("\nExisting users:")
        for i, user in enumerate(users, 1):
            admin_status = "👑 ADMIN" if user.is_admin else "   USER"
            print(f"{i}. {admin_status} - {user.username} ({user.email})")
        
        print("\n" + "=" * 60)
        choice = input("Enter number to make admin (or press Enter to create new): ").strip()
        
        if not choice:
            # Create new admin
            print("\n--- Create New Admin Account ---")
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            
            if not username or not email or not password:
                print("❌ All fields are required!")
                return
            
            # Check if user exists
            if User.query.filter_by(email=email).first():
                print(f"❌ User with email {email} already exists!")
                return
            
            if User.query.filter_by(username=username).first():
                print(f"❌ Username {username} already taken!")
                return
            
            # Create admin user
            admin = User(username=username, email=email)
            admin.set_password(password)
            admin.is_admin = True
            db.session.add(admin)
            db.session.commit()
            
            print(f"\n✅ Admin account created successfully!")
            print(f"\n📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"\n🌐 Login at: http://localhost:5000/login")
            
        else:
            # Make existing user admin
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(users):
                    user = users[idx]
                    user.is_admin = True
                    db.session.commit()
                    print(f"\n✅ {user.username} ({user.email}) is now an admin!")
                    print(f"\n🌐 Login at: http://localhost:5000/login")
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        print("=" * 60)

if __name__ == '__main__':
    create_or_make_admin()
