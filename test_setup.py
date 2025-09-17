"""
Test script to verify the RAG Flask application setup
"""
import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment variables and dependencies."""
    print("🔍 Testing RAG Flask Application Setup...")
    print("=" * 50)
    
    # Test environment variables
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    secret_key = os.getenv('SECRET_KEY')
    
    print("📋 Environment Variables:")
    print(f"   OPENAI_API_KEY: {'✅ Set' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ Not set or default'}")
    print(f"   SECRET_KEY: {'✅ Set' if secret_key and secret_key != 'your_secret_key_here_change_this_in_production' else '❌ Not set or default'}")
    
    # Test imports
    print("\n📦 Testing Dependencies:")
    
    dependencies = [
        ('flask', 'Flask'),
        ('flask_login', 'Flask-Login'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('faiss', 'FAISS'),
        ('openai', 'OpenAI'),
        ('fitz', 'PyMuPDF'),
        ('docx', 'python-docx'),
        ('werkzeug', 'Werkzeug'),
        ('dotenv', 'python-dotenv')
    ]
    
    missing_deps = []
    
    for module, name in dependencies:
        try:
            __import__(module)
            print(f"   {name}: ✅ Installed")
        except ImportError:
            print(f"   {name}: ❌ Missing")
            missing_deps.append(name)
    
    # Test directories
    print("\n📁 Testing Directories:")
    
    directories = ['uploads', 'faiss_indexes', 'templates']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"   {directory}/: ✅ Exists")
        else:
            print(f"   {directory}/: ❌ Missing (will be created automatically)")
    
    # Test template files
    print("\n📄 Testing Template Files:")
    
    templates = [
        'templates/layout.html',
        'templates/index.html',
        'templates/register.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/search.html'
    ]
    
    missing_templates = []
    
    for template in templates:
        if os.path.exists(template):
            print(f"   {template}: ✅ Exists")
        else:
            print(f"   {template}: ❌ Missing")
            missing_templates.append(template)
    
    # Test core files
    print("\n🔧 Testing Core Files:")
    
    core_files = [
        'app.py',
        'models.py',
        'requirements.txt',
        '.env'
    ]
    
    missing_files = []
    
    for file in core_files:
        if os.path.exists(file):
            print(f"   {file}: ✅ Exists")
        else:
            print(f"   {file}: ❌ Missing")
            missing_files.append(file)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Setup Summary:")
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        print("   Run: pip install -r requirements.txt")
    
    if missing_files:
        print(f"❌ Missing core files: {', '.join(missing_files)}")
    
    if missing_templates:
        print(f"❌ Missing templates: {', '.join(missing_templates)}")
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("❌ OpenAI API key not configured")
        print("   Add your API key to .env file")
    
    if not missing_deps and not missing_files and not missing_templates and openai_key and openai_key != 'your_openai_api_key_here':
        print("✅ Setup looks good! You can run the application with: python app.py")
    else:
        print("⚠️  Please fix the issues above before running the application")
    
    print("\n🚀 To start the application:")
    print("   1. Fix any issues shown above")
    print("   2. Run: python app.py")
    print("   3. Open: http://localhost:5000")

if __name__ == '__main__':
    test_environment()
