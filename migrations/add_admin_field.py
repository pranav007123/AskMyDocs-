"""
Database migration to add is_admin field to existing users
Run this script to update the database schema
"""
from app import app, db
from sqlalchemy import text

def migrate_database():
    """Add is_admin column to users table."""
    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(text("PRAGMA table_info(users)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'is_admin' in columns:
                print("✅ is_admin column already exists in users table.")
                return
            
            # Add the column
            print("Adding is_admin column to users table...")
            db.session.execute(text(
                "ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0"
            ))
            db.session.commit()
            print("✅ Successfully added is_admin column to users table!")
            print("\nℹ️  All existing users have been set as regular users (not admin).")
            print("   Use make_admin.py to grant admin privileges to specific users.")
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    print("="*60)
    print("Database Migration: Add Admin Field")
    print("="*60)
    migrate_database()
    print("="*60)
