#!/usr/bin/env python3
"""
Debug script to check FAISS indexes and document processing
"""
import os
import sys
import sqlite3
import numpy as np
import faiss

def check_database():
    """Check database contents"""
    print("=== DATABASE CHECK ===")
    try:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        
        # Check table names first
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"Available tables: {tables}")
        
        # Check users (try different table names)
        users = []
        for table_name in ['users', 'user']:
            try:
                cursor.execute(f"SELECT id, username, email FROM {table_name}")
                users = cursor.fetchall()
                print(f"Users from '{table_name}': {users}")
                break
            except Exception as e:
                print(f"Table '{table_name}' error: {e}")
        
        # Check documents (try different table names)
        documents = []
        for table_name in ['documents', 'document']:
            try:
                cursor.execute(f"SELECT id, user_id, filename, original_name, file_type, chunk_count FROM {table_name}")
                documents = cursor.fetchall()
                print(f"Documents from '{table_name}': {documents}")
                break
            except Exception as e:
                print(f"Table '{table_name}' error: {e}")
        
        conn.close()
        return users, documents
    except Exception as e:
        print(f"Database error: {e}")
        return [], []

def check_faiss_indexes():
    """Check FAISS index files"""
    print("\n=== FAISS INDEX CHECK ===")
    faiss_dir = "faiss_indexes"
    
    if not os.path.exists(faiss_dir):
        print("FAISS directory doesn't exist!")
        return
    
    # Check root level files (old structure)
    root_files = os.listdir(faiss_dir)
    print(f"Root FAISS files: {root_files}")
    
    # Check user-specific directories
    for item in root_files:
        item_path = os.path.join(faiss_dir, item)
        if os.path.isdir(item_path):
            print(f"\nUser directory {item}:")
            user_files = os.listdir(item_path)
            print(f"  Files: {user_files}")
            
            # Check index content
            index_path = os.path.join(item_path, "index.faiss")
            metadata_path = os.path.join(item_path, "metadata.npy")
            
            if os.path.exists(index_path):
                try:
                    index = faiss.read_index(index_path)
                    print(f"  Index vectors: {index.ntotal}")
                except Exception as e:
                    print(f"  Index error: {e}")
            
            if os.path.exists(metadata_path):
                try:
                    metadata = np.load(metadata_path, allow_pickle=True).tolist()
                    print(f"  Metadata entries: {len(metadata)}")
                    if metadata:
                        print(f"  Sample metadata: {metadata[0]}")
                except Exception as e:
                    print(f"  Metadata error: {e}")

def check_uploads():
    """Check uploaded files"""
    print("\n=== UPLOADS CHECK ===")
    uploads_dir = "uploads"
    
    if not os.path.exists(uploads_dir):
        print("Uploads directory doesn't exist!")
        return
    
    files = os.listdir(uploads_dir)
    print(f"Uploaded files: {len(files)}")
    for f in files:
        file_path = os.path.join(uploads_dir, f)
        size = os.path.getsize(file_path)
        print(f"  {f}: {size} bytes")

if __name__ == "__main__":
    print("AskMyDocs Debug Script")
    print("=" * 50)
    
    users, documents = check_database()
    check_uploads()
    check_faiss_indexes()
    
    print("\n=== RECOMMENDATIONS ===")
    if not users:
        print("- No users found. Please register and login first.")
    if not documents:
        print("- No documents found. Please upload documents first.")
    else:
        print(f"- Found {len(documents)} documents for {len(set(d[1] for d in documents))} users")
    
    # Check if FAISS indexes match documents
    faiss_dir = "faiss_indexes"
    if os.path.exists(faiss_dir):
        user_dirs = [d for d in os.listdir(faiss_dir) if os.path.isdir(os.path.join(faiss_dir, d))]
        if user_dirs:
            print(f"- Found FAISS indexes for users: {user_dirs}")
        else:
            print("- No user-specific FAISS directories found. Documents may not be indexed properly.")
