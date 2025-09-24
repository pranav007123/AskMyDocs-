#!/usr/bin/env python3
"""
Comprehensive project health check for RAG application
"""
import os
import sys
import sqlite3
import numpy as np
import faiss
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_environment():
    """Check environment variables and configuration"""
    print("🔧 ENVIRONMENT CHECK")
    print("=" * 50)
    
    # Check .env file
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .env file exists")
        with open(env_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    key = line.split('=')[0]
                    print(f"   📝 {key} configured")
    else:
        print("❌ .env file missing")
    
    # Check Python environment
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    
    return True

def check_dependencies():
    """Check required dependencies"""
    print("\n📦 DEPENDENCIES CHECK")
    print("=" * 50)
    
    required_packages = [
        'flask', 'flask_login', 'flask_migrate', 'sqlalchemy',
        'faiss', 'sentence_transformers', 'numpy', 'openai',
        'fitz', 'docx', 'python-dotenv', 'werkzeug'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        return False
    
    return True

def check_database():
    """Check database integrity"""
    print("\n🗄️  DATABASE CHECK")
    print("=" * 50)
    
    try:
        from app import app, db
        from models import User, Document
        
        with app.app_context():
            # Check tables exist
            try:
                users = User.query.all()
                documents = Document.query.all()
                
                print(f"✅ Database connected")
                print(f"👥 Users: {len(users)}")
                print(f"📄 Documents: {len(documents)}")
                
                for user in users:
                    user_docs = Document.query.filter_by(user_id=user.id).all()
                    print(f"   👤 {user.username} ({user.email}) - {len(user_docs)} documents")
                
                for doc in documents:
                    print(f"   📄 {doc.original_name} - {doc.chunk_count} chunks - User {doc.user_id}")
                
                return True, users, documents
                
            except Exception as e:
                print(f"❌ Database query error: {e}")
                return False, [], []
                
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False, [], []

def check_file_structure():
    """Check file structure and permissions"""
    print("\n📁 FILE STRUCTURE CHECK")
    print("=" * 50)
    
    required_dirs = ['uploads', 'faiss_indexes', 'templates', 'static']
    required_files = ['app.py', 'models.py', 'requirements.txt']
    
    all_good = True
    
    # Check directories
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            files_count = len(os.listdir(dir_name)) if os.path.isdir(dir_name) else 0
            print(f"✅ {dir_name}/ - {files_count} items")
        else:
            print(f"❌ {dir_name}/ - MISSING")
            all_good = False
    
    # Check files
    for file_name in required_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} - {size} bytes")
        else:
            print(f"❌ {file_name} - MISSING")
            all_good = False
    
    return all_good

def check_faiss_indexes(users):
    """Check FAISS indexes"""
    print("\n🔍 FAISS INDEXES CHECK")
    print("=" * 50)
    
    faiss_dir = "faiss_indexes"
    if not os.path.exists(faiss_dir):
        print("❌ FAISS directory missing")
        return False
    
    all_good = True
    
    for user in users:
        user_dir = os.path.join(faiss_dir, str(user.id))
        index_path = os.path.join(user_dir, "index.faiss")
        metadata_path = os.path.join(user_dir, "metadata.npy")
        
        print(f"\n👤 User {user.username} (ID: {user.id}):")
        
        if os.path.exists(index_path):
            try:
                index = faiss.read_index(index_path)
                print(f"   ✅ FAISS index - {index.ntotal} vectors")
            except Exception as e:
                print(f"   ❌ FAISS index error: {e}")
                all_good = False
        else:
            print(f"   ❌ FAISS index missing")
            all_good = False
        
        if os.path.exists(metadata_path):
            try:
                metadata = np.load(metadata_path, allow_pickle=True).tolist()
                print(f"   ✅ Metadata - {len(metadata)} entries")
                
                # Check metadata structure
                if metadata:
                    sample = metadata[0]
                    required_keys = ['document_id', 'chunk_index', 'text', 'filename']
                    missing_keys = [key for key in required_keys if key not in sample]
                    if missing_keys:
                        print(f"   ⚠️  Missing metadata keys: {missing_keys}")
                    else:
                        print(f"   ✅ Metadata structure valid")
                
            except Exception as e:
                print(f"   ❌ Metadata error: {e}")
                all_good = False
        else:
            print(f"   ❌ Metadata missing")
            all_good = False
    
    return all_good

def check_uploads():
    """Check uploaded files"""
    print("\n📤 UPLOADS CHECK")
    print("=" * 50)
    
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        print("❌ Uploads directory missing")
        return False
    
    files = os.listdir(uploads_dir)
    print(f"📁 Found {len(files)} uploaded files")
    
    total_size = 0
    for file in files:
        file_path = os.path.join(uploads_dir, file)
        size = os.path.getsize(file_path)
        total_size += size
        size_mb = size / (1024 * 1024)
        print(f"   📄 {file} - {size_mb:.2f} MB")
    
    total_mb = total_size / (1024 * 1024)
    print(f"💾 Total upload size: {total_mb:.2f} MB")
    
    return True

def test_embedding_model():
    """Test sentence transformer model"""
    print("\n🤖 EMBEDDING MODEL CHECK")
    print("=" * 50)
    
    try:
        from sentence_transformers import SentenceTransformer
        
        print("🔄 Loading embedding model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Test encoding
        test_text = "This is a test sentence for embedding."
        embedding = model.encode([test_text])
        
        print(f"✅ Model loaded successfully")
        print(f"📐 Embedding dimension: {embedding.shape[1]}")
        print(f"🔢 Test embedding shape: {embedding.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Embedding model error: {e}")
        return False

def generate_health_report():
    """Generate comprehensive health report"""
    print("\n" + "=" * 80)
    print("🏥 COMPREHENSIVE HEALTH REPORT")
    print("=" * 80)
    
    # Run all checks
    env_ok = check_environment()
    deps_ok = check_dependencies()
    db_ok, users, documents = check_database()
    files_ok = check_file_structure()
    faiss_ok = check_faiss_indexes(users) if users else False
    uploads_ok = check_uploads()
    embedding_ok = test_embedding_model()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 50)
    
    checks = [
        ("Environment", env_ok),
        ("Dependencies", deps_ok),
        ("Database", db_ok),
        ("File Structure", files_ok),
        ("FAISS Indexes", faiss_ok),
        ("Uploads", uploads_ok),
        ("Embedding Model", embedding_ok)
    ]
    
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    
    for check_name, ok in checks:
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{check_name:15} {status}")
    
    print(f"\n🎯 Overall Score: {passed}/{total} ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL SYSTEMS GO! Your RAG project is fully operational!")
    elif passed >= total * 0.8:
        print("⚠️  Minor issues detected. Project should work with some limitations.")
    else:
        print("🚨 Major issues detected. Project may not function properly.")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 50)
    
    if not deps_ok:
        print("📦 Install missing dependencies: pip install -r requirements.txt")
    
    if not db_ok:
        print("🗄️  Initialize database: python init_database.py")
    
    if not faiss_ok and users:
        print("🔍 Rebuild FAISS indexes: Re-upload documents or run index rebuild")
    
    if not uploads_ok:
        print("📤 Check uploads directory permissions")
    
    print(f"\n⏰ Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    generate_health_report()
