#!/usr/bin/env python3
"""
Final comprehensive test of RAG functionality
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_search_functionality():
    """Test the search functionality"""
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 50)
    
    try:
        from app import app
        from models import User, Document
        
        with app.app_context():
            # Get test user
            user = User.query.filter_by(email='test@example.com').first()
            if not user:
                print("ERROR: Test user not found")
                return False
            
            print(f"Test user: {user.username} (ID: {user.id})")
            
            # Get user documents
            documents = Document.query.filter_by(user_id=user.id).all()
            print(f"User documents: {len(documents)}")
            
            if not documents:
                print("ERROR: No documents found for test user")
                return False
            
            # Test search function
            from app import search_faiss_index, highlight_relevant_content
            
            test_queries = [
                "What is this document about?",
                "Summarize the main points",
                "Tell me about the content"
            ]
            
            for query in test_queries:
                print(f"\nTesting query: '{query}'")
                
                # Search FAISS index
                results = search_faiss_index(user.id, query, k=3)
                print(f"  Found {len(results)} results")
                
                if results:
                    for i, result in enumerate(results):
                        score = result['score']
                        filename = result['filename']
                        text_preview = result['text'][:100] + "..." if len(result['text']) > 100 else result['text']
                        print(f"    {i+1}. {filename} (Score: {score:.3f})")
                        print(f"       Preview: {text_preview}")
                        
                        # Test highlighting
                        if 'highlighted_text' in result:
                            has_highlights = '<mark class="search-highlight">' in result['highlighted_text']
                            print(f"       Highlighting: {'YES' if has_highlights else 'NO'}")
                else:
                    print("  No results found")
            
            return True
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_rag_generation():
    """Test RAG response generation"""
    print("\nTESTING RAG GENERATION")
    print("=" * 50)
    
    try:
        from app import generate_rag_response
        
        # Mock results for testing
        mock_results = [
            {
                'text': 'This is a test document about Flask applications and web development.',
                'filename': 'test.pdf',
                'score': 0.85
            },
            {
                'text': 'The document covers authentication, database management, and user interfaces.',
                'filename': 'test.pdf',
                'score': 0.75
            }
        ]
        
        test_query = "What is this document about?"
        
        print(f"Testing query: '{test_query}'")
        print("Mock results provided...")
        
        # Generate response
        answer = generate_rag_response(test_query, mock_results)
        
        if answer and len(answer) > 10:
            print(f"Generated answer: {answer[:200]}...")
            print("RAG generation: SUCCESS")
            return True
        else:
            print(f"Generated answer: {answer}")
            print("RAG generation: FAILED - Answer too short or empty")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_final_tests():
    """Run all final tests"""
    print("FINAL RAG PROJECT TESTS")
    print("=" * 80)
    
    # Test search
    search_ok = test_search_functionality()
    
    # Test RAG generation
    rag_ok = test_rag_generation()
    
    # Summary
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)
    
    tests = [
        ("Search Functionality", search_ok),
        ("RAG Generation", rag_ok)
    ]
    
    passed = sum(1 for _, ok in tests if ok)
    total = len(tests)
    
    for test_name, ok in tests:
        status = "PASS" if ok else "FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nSUCCESS: Your RAG project is fully functional!")
        print("\nYou can now:")
        print("1. Login at http://localhost:5000 with:")
        print("   Email: test@example.com")
        print("   Password: password123")
        print("2. Upload new documents")
        print("3. Search your documents with AI-powered answers")
        print("4. View highlighted source references")
    else:
        print("\nWARNING: Some functionality may not work properly")
        print("Check the error messages above for details")

if __name__ == "__main__":
    run_final_tests()
