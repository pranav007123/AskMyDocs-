#!/usr/bin/env python3
"""
Fix existing uploaded files by adding them to the database
"""
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Document

def fix_existing_data():
    """Add existing uploaded files to database"""
    print("Fixing existing data...")
    
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        # Get or create test user
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
            print(f"Created user: {user.username} (ID: {user.id})")
        else:
            print(f"Using existing user: {user.username} (ID: {user.id})")
        
        # Check uploads directory
        uploads_dir = "uploads"
        if not os.path.exists(uploads_dir):
            print("No uploads directory found")
            return
        
        uploaded_files = os.listdir(uploads_dir)
        print(f"Found {len(uploaded_files)} uploaded files")
        
        # Add files to database if they don't exist
        for filename in uploaded_files:
            if filename.endswith(('.pdf', '.docx', '.txt')):
                # Check if document already exists
                existing_doc = Document.query.filter_by(filename=filename).first()
                if not existing_doc:
                    # Determine file type
                    file_extension = filename.split('.')[-1].lower()
                    
                    # Create document record
                    document = Document(
                        user_id=user.id,
                        filename=filename,
                        original_name=f"uploaded_document.{file_extension}",
                        file_type=file_extension,
                        chunk_count=0  # Will be updated when we reprocess
                    )
                    db.session.add(document)
                    print(f"Added document: {filename}")
                else:
                    print(f"Document already exists: {filename}")
        
        db.session.commit()
        
        # Show final state
        all_users = User.query.all()
        all_docs = Document.query.all()
        print(f"\nFinal state:")
        print(f"Users: {len(all_users)}")
        print(f"Documents: {len(all_docs)}")
        
        for doc in all_docs:
            print(f"  - {doc.original_name} (User: {doc.user_id}, File: {doc.filename})")

if __name__ == "__main__":
    fix_existing_data()
    print("Data fix complete!")
