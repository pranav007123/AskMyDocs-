"""
Script to make a user an admin
Usage: python make_admin.py <email>
"""
import sys
from app import app, db, User

def make_admin(email):
    """Make a user an admin by email."""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found.")
            print("\nAvailable users:")
            all_users = User.query.all()
            for u in all_users:
                admin_status = "Admin" if u.is_admin else "User"
                print(f"  - {u.email} ({u.username}) [{admin_status}]")
            return False
        
        if user.is_admin:
            print(f"✅ User {user.username} ({email}) is already an admin.")
            return True
        
        user.is_admin = True
        db.session.commit()
        print(f"✅ Successfully made {user.username} ({email}) an admin!")
        return True

def list_users():
    """List all users and their admin status."""
    with app.app_context():
        users = User.query.all()
        
        if not users:
            print("No users found in database.")
            return
        
        print("\n" + "="*60)
        print("All Users:")
        print("="*60)
        for user in users:
            admin_badge = "👑 ADMIN" if user.is_admin else "   USER"
            print(f"{admin_badge} | {user.email:30s} | {user.username}")
        print("="*60 + "\n")

def revoke_admin(email):
    """Revoke admin privileges from a user."""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found.")
            return False
        
        if not user.is_admin:
            print(f"ℹ️  User {user.username} ({email}) is not an admin.")
            return True
        
        user.is_admin = False
        db.session.commit()
        print(f"✅ Successfully revoked admin privileges from {user.username} ({email})!")
        return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python make_admin.py <email>          - Make user an admin")
        print("  python make_admin.py list             - List all users")
        print("  python make_admin.py revoke <email>   - Revoke admin privileges")
        print("\nExamples:")
        print("  python make_admin.py admin@test.com")
        print("  python make_admin.py list")
        print("  python make_admin.py revoke user@test.com")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_users()
    elif command == 'revoke':
        if len(sys.argv) < 3:
            print("❌ Please provide an email address to revoke admin from.")
            print("Usage: python make_admin.py revoke <email>")
            sys.exit(1)
        revoke_admin(sys.argv[2])
    else:
        # Treat first argument as email
        make_admin(command)
