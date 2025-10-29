"""
Quick script to set admin by email
Usage: python set_admin.py <email>
"""
import sys
from app import app, db, User
from sqlalchemy import text

def set_admin(email=None):
    """Make a user admin."""
    with app.app_context():
        # Add column if needed
        try:
            db.session.execute(text("SELECT is_admin FROM users LIMIT 1"))
        except:
            db.session.rollback()
            db.session.execute(text(
                "ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"
            ))
            db.session.commit()
            print("Database updated with is_admin column")
        
        # List users if no email provided
        if not email:
            print("\n=== Available Users ===")
            users = User.query.all()
            for user in users:
                admin = "ADMIN" if hasattr(user, 'is_admin') and user.is_admin else "USER"
                print(f"  [{admin}] {user.email} ({user.username})")
            print("\nUsage: python set_admin.py <email>")
            print("Example: python set_admin.py test@example.com")
            return
        
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"ERROR: User with email '{email}' not found!")
            print("\nAvailable users:")
            for u in User.query.all():
                print(f"  - {u.email}")
            return
        
        user.is_admin = True
        db.session.commit()
        
        print(f"\nSUCCESS! {user.username} is now an admin!")
        print(f"\nLogin Details:")
        print(f"  Email: {user.email}")
        print(f"  Go to: http://localhost:5000/login")
        print(f"\nAfter login, you'll see 'Admin' in the navbar.")

if __name__ == '__main__':
    email = sys.argv[1] if len(sys.argv) > 1 else None
    set_admin(email)
