"""
Database initialization script for RAG Flask Application
"""
import os
from app import app, db

def init_database():
    """Initialize the database with tables."""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")
        print(f"Database file: {os.path.abspath('rag_app.db')}")

if __name__ == '__main__':
    init_database()
