#!/usr/bin/env python3
"""
Update chunk counts for existing documents
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Document

def update_chunk_counts():
    """Update chunk counts based on FAISS metadata"""
    print("Updating chunk counts...")
    
    with app.app_context():
        # Get all documents
        documents = Document.query.all()
        print(f"Found {len(documents)} documents")
        
        for doc in documents:
            print(f"Processing document: {doc.original_name} (ID: {doc.id})")
            
            # Check FAISS metadata for this user
            faiss_dir = f"faiss_indexes/{doc.user_id}"
            metadata_path = os.path.join(faiss_dir, "metadata.npy")
            
            if os.path.exists(metadata_path):
                try:
                    import numpy as np
                    metadata = np.load(metadata_path, allow_pickle=True).tolist()
                    
                    # Count chunks for this document
                    doc_chunks = [m for m in metadata if m.get('document_id') == doc.id]
                    chunk_count = len(doc_chunks)
                    
                    print(f"  Found {chunk_count} chunks in FAISS")
                    
                    # Update document
                    doc.chunk_count = chunk_count
                    
                except Exception as e:
                    print(f"  Error reading metadata: {e}")
            else:
                print(f"  No FAISS metadata found at {metadata_path}")
        
        # Commit changes
        db.session.commit()
        print("Updated chunk counts")
        
        # Show final state
        for doc in Document.query.all():
            print(f"  {doc.original_name}: {doc.chunk_count} chunks")

if __name__ == "__main__":
    update_chunk_counts()
    print("Chunk count update complete!")
