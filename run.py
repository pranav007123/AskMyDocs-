"""
Simple run script for the RAG Flask Application
"""
import os
import sys
from dotenv import load_dotenv

def check_setup():
    """Check if the application is properly set up."""
    load_dotenv()
    
    # Determine LLM provider and validate required API key
    llm_provider = os.getenv('LLM_PROVIDER', 'openai').lower().strip()
    openai_key = os.getenv('OPENAI_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    print(f"[SETUP] LLM_PROVIDER: {llm_provider}")
    print(f"[SETUP] OPENAI_API_KEY configured: {bool(openai_key)}")
    print(f"[SETUP] GEMINI_API_KEY configured: {bool(gemini_key)}")

    if llm_provider == 'openai':
        if not openai_key or openai_key == 'your_openai_api_key_here':
            print("❌ Error: OpenAI API key not configured!")
            print("Please add your OpenAI API key to the .env file:")
            print("OPENAI_API_KEY=your_actual_api_key_here")
            return False
    elif llm_provider == 'gemini':
        if not gemini_key:
            print("❌ Error: Gemini selected but GEMINI_API_KEY not configured!")
            print("Please add your Gemini API key to the .env file:")
            print("GEMINI_API_KEY=your_actual_api_key_here")
            return False
    else:
        print(f"❌ Error: Unknown LLM_PROVIDER '{llm_provider}'. Use 'openai' or 'gemini'.")
        return False
    
    # Check for required files
    required_files = ['app.py', 'models.py', '.env']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: Required file {file} not found!")
            return False
    
    return True

def create_directories():
    """Create necessary directories."""
    directories = ['uploads', 'faiss_indexes']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory {directory}/ ready")

def main():
    """Main function to run the application."""
    print("🚀 Starting RAG Flask Application...")
    print("=" * 40)
    
    # Check setup
    if not check_setup():
        print("\n❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Import and run the app
    try:
        from app import app, db
        
        # Initialize database
        with app.app_context():
            db.create_all()
            print("✅ Database initialized")
        
        print("✅ Setup complete!")
        print("\n🌐 Starting server...")
        print("📍 Application will be available at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 40)
        
        # Run the application
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
