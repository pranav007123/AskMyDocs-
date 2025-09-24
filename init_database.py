#!/usr/bin/env python3
"""
Initialize the database properly
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Document

def init_database():
    """Initialize database with all tables"""
    print("Initializing database...")
    
    with app.app_context():
        # Drop all tables first (clean slate)
        db.drop_all()
        print("Dropped existing tables")
        
        # Create all tables
        db.create_all()
        print("Created all tables")
        
        # Verify tables were created
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created tables: {tables}")
        
        # Create a test user if needed
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(username='testuser', email='test@example.com')
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print(f"Created test user with ID: {test_user.id}")
        else:
            print(f"Test user already exists with ID: {test_user.id}")

if __name__ == "__main__":
    init_database()
    print("Database initialization complete!")
