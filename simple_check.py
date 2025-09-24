#!/usr/bin/env python3
"""
Simple project health check for RAG application
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_project():
    """Check project health"""
    print("RAG PROJECT HEALTH CHECK")
    print("=" * 50)
    
    # 1. Check database
    print("\n1. DATABASE CHECK")
    try:
        from app import app, db
        from models import User, Document
        
        with app.app_context():
            users = User.query.all()
            documents = Document.query.all()
            
            print(f"   Users: {len(users)}")
            print(f"   Documents: {len(documents)}")
            
            for user in users:
                user_docs = Document.query.filter_by(user_id=user.id).all()
                print(f"   - {user.username}: {len(user_docs)} docs")
            
            db_status = "OK"
    except Exception as e:
        print(f"   ERROR: {e}")
        db_status = "FAILED"
        users = []
        documents = []
    
    # 2. Check files
    print("\n2. FILE STRUCTURE CHECK")
    required_dirs = ['uploads', 'faiss_indexes', 'templates', 'static']
    required_files = ['app.py', 'models.py', 'requirements.txt']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            count = len(os.listdir(dir_name)) if os.path.isdir(dir_name) else 0
            print(f"   {dir_name}/: {count} items")
        else:
            print(f"   {dir_name}/: MISSING")
    
    for file_name in required_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"   {file_name}: {size} bytes")
        else:
            print(f"   {file_name}: MISSING")
    
    # 3. Check FAISS indexes
    print("\n3. FAISS INDEXES CHECK")
    faiss_dir = "faiss_indexes"
    if os.path.exists(faiss_dir):
        for user in users:
            user_dir = os.path.join(faiss_dir, str(user.id))
            if os.path.exists(user_dir):
                files = os.listdir(user_dir)
                print(f"   User {user.id}: {files}")
                
                # Check index content
                index_path = os.path.join(user_dir, "index.faiss")
                if os.path.exists(index_path):
                    try:
                        import faiss
                        index = faiss.read_index(index_path)
                        print(f"     Index vectors: {index.ntotal}")
                    except Exception as e:
                        print(f"     Index error: {e}")
            else:
                print(f"   User {user.id}: No directory")
    else:
        print("   FAISS directory missing")
    
    # 4. Check uploads
    print("\n4. UPLOADS CHECK")
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        files = os.listdir(uploads_dir)
        print(f"   Files: {len(files)}")
        total_size = 0
        for f in files:
            size = os.path.getsize(os.path.join(uploads_dir, f))
            total_size += size
            print(f"   - {f}: {size/1024/1024:.1f} MB")
        print(f"   Total: {total_size/1024/1024:.1f} MB")
    else:
        print("   Uploads directory missing")
    
    # 5. Test embedding model
    print("\n5. EMBEDDING MODEL CHECK")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_embedding = model.encode(["test"])
        print(f"   Model loaded: {test_embedding.shape}")
        embedding_status = "OK"
    except Exception as e:
        print(f"   ERROR: {e}")
        embedding_status = "FAILED"
    
    # 6. Check environment
    print("\n6. ENVIRONMENT CHECK")
    env_file = ".env"
    if os.path.exists(env_file):
        print("   .env file exists")
        with open(env_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
            for line in lines:
                key = line.split('=')[0]
                print(f"   - {key} configured")
    else:
        print("   .env file missing")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Database: {db_status}")
    print(f"Embedding Model: {embedding_status}")
    print(f"Users: {len(users)}")
    print(f"Documents: {len(documents)}")
    
    if len(users) > 0 and len(documents) > 0 and db_status == "OK" and embedding_status == "OK":
        print("\nSTATUS: PROJECT IS READY!")
        print("You can now:")
        print("1. Login with test@example.com / password123")
        print("2. Upload new documents")
        print("3. Search your documents")
        print("4. Get AI-powered answers")
    else:
        print("\nSTATUS: ISSUES DETECTED")
        if len(users) == 0:
            print("- No users found. Run: python fix_existing_data.py")
        if len(documents) == 0:
            print("- No documents found. Upload some documents")
        if db_status != "OK":
            print("- Database issues. Run: python init_database.py")
        if embedding_status != "OK":
            print("- Embedding model issues. Check dependencies")

if __name__ == "__main__":
    check_project()
