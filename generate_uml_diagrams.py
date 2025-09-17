"""
Generate UML diagrams for RAG Flask Application
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import os

# Set up matplotlib for better rendering
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'

def create_system_architecture():
    """Create System Architecture Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'RAG System Architecture', fontsize=18, fontweight='bold', ha='center')
    
    # User/Browser
    user_box = FancyBboxPatch((0.5, 7.5), 2, 1, boxstyle="round,pad=0.1", 
                              facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(1.5, 8, 'User Browser\n(Bootstrap UI)', ha='center', va='center', fontweight='bold')
    
    # Flask App
    flask_box = FancyBboxPatch((4, 7), 3, 2, boxstyle="round,pad=0.1", 
                               facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(flask_box)
    ax.text(5.5, 8, 'Flask Application\n(app.py)\n• Routes & Auth\n• RAG Logic', 
            ha='center', va='center', fontweight='bold')
    
    # Database
    db_box = FancyBboxPatch((8.5, 8), 2, 1, boxstyle="round,pad=0.1", 
                            facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(db_box)
    ax.text(9.5, 8.5, 'SQLite DB\n(Users, Docs)', ha='center', va='center', fontweight='bold')
    
    # File Storage
    files_box = FancyBboxPatch((8.5, 6.5), 2, 1, boxstyle="round,pad=0.1", 
                               facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(files_box)
    ax.text(9.5, 7, 'File Storage\n(/uploads)', ha='center', va='center', fontweight='bold')
    
    # Sentence Transformers
    embed_box = FancyBboxPatch((4, 4.5), 3, 1.5, boxstyle="round,pad=0.1", 
                               facecolor='lightsteelblue', edgecolor='black', linewidth=2)
    ax.add_patch(embed_box)
    ax.text(5.5, 5.25, 'Sentence Transformers\n(all-MiniLM-L6-v2)\n384-dim embeddings', 
            ha='center', va='center', fontweight='bold')
    
    # FAISS Vector Store
    faiss_box = FancyBboxPatch((8.5, 4.5), 2.5, 1.5, boxstyle="round,pad=0.1", 
                               facecolor='plum', edgecolor='black', linewidth=2)
    ax.add_patch(faiss_box)
    ax.text(9.75, 5.25, 'FAISS Index\n(Per-user)\nCosine Similarity', 
            ha='center', va='center', fontweight='bold')
    
    # LLM (Gemini/OpenAI)
    llm_box = FancyBboxPatch((4, 2), 3, 1.5, boxstyle="round,pad=0.1", 
                             facecolor='gold', edgecolor='black', linewidth=2)
    ax.add_patch(llm_box)
    ax.text(5.5, 2.75, 'LLM Backend\nGemini/OpenAI\nRAG Generation', 
            ha='center', va='center', fontweight='bold')
    
    # Arrows
    arrows = [
        # User to Flask
        ((2.5, 8), (4, 8)),
        # Flask to DB
        ((7, 8.5), (8.5, 8.5)),
        # Flask to Files
        ((7, 7.5), (8.5, 7)),
        # Flask to Embeddings
        ((5.5, 7), (5.5, 6)),
        # Embeddings to FAISS
        ((7, 5.25), (8.5, 5.25)),
        # Flask to LLM
        ((5.5, 7), (5.5, 3.5)),
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='darkblue'))
    
    # Add flow labels
    ax.text(3, 8.3, 'HTTP Requests', ha='center', fontsize=9, color='darkblue')
    ax.text(7.7, 8.7, 'Store', ha='center', fontsize=9, color='darkblue')
    ax.text(7.7, 7.2, 'Save Files', ha='center', fontsize=9, color='darkblue')
    ax.text(5.8, 6.5, 'Embed', ha='center', fontsize=9, color='darkblue')
    ax.text(7.7, 5.5, 'Index', ha='center', fontsize=9, color='darkblue')
    ax.text(5.8, 4, 'Generate', ha='center', fontsize=9, color='darkblue')
    
    plt.tight_layout()
    plt.savefig('RAG_System_Architecture.jpg', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_class_diagram():
    """Create Class Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, 'RAG Application Class Diagram', fontsize=16, fontweight='bold', ha='center')
    
    # User Class
    user_box = FancyBboxPatch((0.5, 4.5), 3, 2.5, boxstyle="round,pad=0.1", 
                              facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(user_box)
    ax.text(2, 6.5, 'User', ha='center', fontweight='bold', fontsize=12)
    ax.text(2, 6, '- id: int\n- username: str\n- email: str\n- password_hash: str\n- created_at: datetime', 
            ha='center', va='center', fontsize=9)
    ax.text(2, 5, '+ set_password()\n+ check_password()', ha='center', va='center', fontsize=9)
    
    # Document Class
    doc_box = FancyBboxPatch((4.5, 4.5), 3, 2.5, boxstyle="round,pad=0.1", 
                             facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(doc_box)
    ax.text(6, 6.5, 'Document', ha='center', fontweight='bold', fontsize=12)
    ax.text(6, 6, '- id: int\n- user_id: int (FK)\n- filename: str\n- original_name: str\n- file_type: str\n- uploaded_at: datetime\n- chunk_count: int', 
            ha='center', va='center', fontsize=9)
    
    # Flask App Class
    app_box = FancyBboxPatch((8.5, 4.5), 3, 2.5, boxstyle="round,pad=0.1", 
                             facecolor='lightyellow', edgecolor='black', linewidth=2)
    ax.add_patch(app_box)
    ax.text(10, 6.5, 'FlaskApp', ha='center', fontweight='bold', fontsize=12)
    ax.text(10, 6, '+ register()\n+ login()\n+ upload_file()\n+ search()\n+ delete_document()', 
            ha='center', va='center', fontsize=9)
    ax.text(10, 5.2, '+ extract_text_from_file()\n+ chunk_text()\n+ generate_rag_response()', 
            ha='center', va='center', fontsize=9)
    
    # RAG Engine Class
    rag_box = FancyBboxPatch((4.5, 1.5), 3, 2.5, boxstyle="round,pad=0.1", 
                             facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(rag_box)
    ax.text(6, 3.5, 'RAGEngine', ha='center', fontweight='bold', fontsize=12)
    ax.text(6, 3, '- embedding_model\n- faiss_index\n- llm_client', ha='center', va='center', fontsize=9)
    ax.text(6, 2.2, '+ add_document_to_faiss()\n+ search_faiss_index()\n+ generate_response()', 
            ha='center', va='center', fontsize=9)
    
    # Relationships
    # User -> Document (1:N)
    ax.annotate('', xy=(4.5, 5.75), xytext=(3.5, 5.75),
               arrowprops=dict(arrowstyle='->', lw=2, color='darkred'))
    ax.text(4, 6, '1:N', ha='center', fontsize=9, color='darkred')
    
    # FlaskApp -> RAGEngine
    ax.annotate('', xy=(7.5, 2.75), xytext=(8.5, 4.5),
               arrowprops=dict(arrowstyle='->', lw=2, color='darkgreen'))
    ax.text(8, 3.5, 'uses', ha='center', fontsize=9, color='darkgreen')
    
    plt.tight_layout()
    plt.savefig('RAG_Class_Diagram.jpg', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_sequence_diagram():
    """Create Sequence Diagram for RAG Flow"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'RAG Query Sequence Diagram', fontsize=16, fontweight='bold', ha='center')
    
    # Actors
    actors = ['User', 'Flask App', 'FAISS', 'Embeddings', 'LLM']
    x_positions = [1, 4, 7, 10, 13]
    
    # Draw actor boxes
    for i, (actor, x) in enumerate(zip(actors, x_positions)):
        actor_box = FancyBboxPatch((x-0.7, 8.5), 1.4, 0.8, boxstyle="round,pad=0.1", 
                                   facecolor='lightblue', edgecolor='black', linewidth=2)
        ax.add_patch(actor_box)
        ax.text(x, 8.9, actor, ha='center', va='center', fontweight='bold')
        
        # Lifelines
        ax.plot([x, x], [8.5, 1], 'k--', alpha=0.5)
    
    # Messages
    messages = [
        (1, 4, 7.8, "1: Submit query"),
        (4, 10, 7.4, "2: Embed query"),
        (10, 4, 7.0, "3: Return query vector"),
        (4, 7, 6.6, "4: Search similar chunks"),
        (7, 4, 6.2, "5: Return top-k chunks"),
        (4, 13, 5.8, "6: Generate answer (query + context)"),
        (13, 4, 5.4, "7: Return AI response"),
        (4, 1, 5.0, "8: Display answer + sources"),
    ]
    
    for start_x, end_x, y, message in messages:
        # Arrow
        ax.annotate('', xy=(end_x-0.1, y), xytext=(start_x+0.1, y),
                   arrowprops=dict(arrowstyle='->', lw=1.5, color='darkblue'))
        # Message text
        mid_x = (start_x + end_x) / 2
        ax.text(mid_x, y+0.15, message, ha='center', fontsize=9, color='darkblue')
    
    # Add activation boxes
    activations = [
        (4, 7.8, 5.0),  # Flask App
        (10, 7.4, 7.0),  # Embeddings
        (7, 6.6, 6.2),   # FAISS
        (13, 5.8, 5.4),  # LLM
    ]
    
    for x, top, bottom in activations:
        activation_box = FancyBboxPatch((x-0.1, bottom), 0.2, top-bottom, 
                                        facecolor='yellow', alpha=0.7, edgecolor='black')
        ax.add_patch(activation_box)
    
    plt.tight_layout()
    plt.savefig('RAG_Sequence_Diagram.jpg', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_deployment_diagram():
    """Create Deployment Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Title
    ax.text(6, 7.5, 'RAG Application Deployment Diagram', fontsize=16, fontweight='bold', ha='center')
    
    # Client Machine
    client_box = FancyBboxPatch((0.5, 5), 3, 2, boxstyle="round,pad=0.1", 
                                facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(client_box)
    ax.text(2, 6.5, 'Client Machine', ha='center', fontweight='bold', fontsize=12)
    ax.text(2, 6, '<<device>>\nWeb Browser', ha='center', va='center', fontsize=10)
    ax.text(2, 5.5, 'Bootstrap UI\nHTML/CSS/JS', ha='center', va='center', fontsize=9)
    
    # Server Machine
    server_box = FancyBboxPatch((5, 4), 6, 3.5, boxstyle="round,pad=0.1", 
                                facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(server_box)
    ax.text(8, 7, 'Application Server', ha='center', fontweight='bold', fontsize=12)
    
    # Flask App inside server
    flask_inner = FancyBboxPatch((5.5, 5.5), 2, 1.5, boxstyle="round,pad=0.05", 
                                 facecolor='lightyellow', edgecolor='black', linewidth=1)
    ax.add_patch(flask_inner)
    ax.text(6.5, 6.25, 'Flask App\n(app.py)', ha='center', va='center', fontsize=10)
    
    # Database inside server
    db_inner = FancyBboxPatch((8, 5.5), 1.5, 1.5, boxstyle="round,pad=0.05", 
                              facecolor='lightcoral', edgecolor='black', linewidth=1)
    ax.add_patch(db_inner)
    ax.text(8.75, 6.25, 'SQLite\nDatabase', ha='center', va='center', fontsize=10)
    
    # File System inside server
    fs_inner = FancyBboxPatch((5.5, 4.2), 2, 1, boxstyle="round,pad=0.05", 
                              facecolor='lightsteelblue', edgecolor='black', linewidth=1)
    ax.add_patch(fs_inner)
    ax.text(6.5, 4.7, 'File System\n(/uploads, /faiss)', ha='center', va='center', fontsize=10)
    
    # FAISS inside server
    faiss_inner = FancyBboxPatch((8, 4.2), 1.5, 1, boxstyle="round,pad=0.05", 
                                 facecolor='plum', edgecolor='black', linewidth=1)
    ax.add_patch(faiss_inner)
    ax.text(8.75, 4.7, 'FAISS\nIndexes', ha='center', va='center', fontsize=10)
    
    # External APIs
    api_box = FancyBboxPatch((5, 1.5), 6, 1.5, boxstyle="round,pad=0.1", 
                             facecolor='gold', edgecolor='black', linewidth=2)
    ax.add_patch(api_box)
    ax.text(8, 2.7, 'External APIs', ha='center', fontweight='bold', fontsize=12)
    ax.text(6.5, 2.2, 'Gemini API', ha='center', va='center', fontsize=10)
    ax.text(9.5, 2.2, 'OpenAI API', ha='center', va='center', fontsize=10)
    
    # Connections
    # Client to Server
    ax.annotate('', xy=(5, 6), xytext=(3.5, 6),
               arrowprops=dict(arrowstyle='<->', lw=2, color='darkblue'))
    ax.text(4.25, 6.3, 'HTTPS', ha='center', fontsize=9, color='darkblue')
    
    # Server to APIs
    ax.annotate('', xy=(8, 3), xytext=(8, 4),
               arrowprops=dict(arrowstyle='<->', lw=2, color='darkgreen'))
    ax.text(8.5, 3.5, 'API Calls', ha='center', fontsize=9, color='darkgreen')
    
    plt.tight_layout()
    plt.savefig('RAG_Deployment_Diagram.jpg', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

def create_use_case_diagram():
    """Create Use Case Diagram"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(6, 9.5, 'RAG Application Use Case Diagram', fontsize=16, fontweight='bold', ha='center')
    
    # System boundary
    system_box = FancyBboxPatch((2, 1), 8, 7.5, boxstyle="round,pad=0.2", 
                                facecolor='none', edgecolor='black', linewidth=2)
    ax.add_patch(system_box)
    ax.text(6, 8.2, 'RAG System', ha='center', fontweight='bold', fontsize=14)
    
    # Actor
    actor_box = FancyBboxPatch((0.2, 4.5), 1.2, 1, boxstyle="round,pad=0.1", 
                               facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(actor_box)
    ax.text(0.8, 5, 'User', ha='center', va='center', fontweight='bold')
    
    # Use cases
    use_cases = [
        (4, 7, 'Register'),
        (6, 7, 'Login'),
        (8, 7, 'Logout'),
        (4, 6, 'Upload Document'),
        (6, 6, 'View Documents'),
        (8, 6, 'Delete Document'),
        (4, 5, 'Search Documents'),
        (6, 5, 'Ask Questions'),
        (8, 5, 'View Sources'),
        (4, 4, 'Download Document'),
        (6, 4, 'Manage Profile'),
        (8, 4, 'View History'),
    ]
    
    for x, y, case in use_cases:
        case_box = patches.Ellipse((x, y), 1.5, 0.6, facecolor='lightyellow', 
                                   edgecolor='black', linewidth=1)
        ax.add_patch(case_box)
        ax.text(x, y, case, ha='center', va='center', fontsize=9, fontweight='bold')
        
        # Connect to actor
        ax.plot([1.4, x-0.75], [5, y], 'k-', alpha=0.6, linewidth=1)
    
    # External system
    ext_box = FancyBboxPatch((10.5, 2.5), 1.2, 2, boxstyle="round,pad=0.1", 
                             facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax.add_patch(ext_box)
    ax.text(11.1, 3.5, 'LLM API\n(Gemini/\nOpenAI)', ha='center', va='center', fontweight='bold')
    
    # Connect search to external API
    ax.plot([8.75, 10.5], [5, 3.5], 'k--', alpha=0.6, linewidth=1)
    ax.text(9.5, 4.2, '<<uses>>', ha='center', fontsize=8, style='italic')
    
    plt.tight_layout()
    plt.savefig('RAG_Use_Case_Diagram.jpg', dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == "__main__":
    print("Generating UML diagrams...")
    
    create_system_architecture()
    print("System Architecture Diagram created")
    
    create_class_diagram()
    print("Class Diagram created")
    
    create_sequence_diagram()
    print("Sequence Diagram created")
    
    create_deployment_diagram()
    print("Deployment Diagram created")
    
    create_use_case_diagram()
    print("Use Case Diagram created")
    
    print("\nAll UML diagrams generated as JPG files:")
    diagrams = [
        "RAG_System_Architecture.jpg",
        "RAG_Class_Diagram.jpg", 
        "RAG_Sequence_Diagram.jpg",
        "RAG_Deployment_Diagram.jpg",
        "RAG_Use_Case_Diagram.jpg"
    ]
    
    for diagram in diagrams:
        if os.path.exists(diagram):
            print(f"  [OK] {diagram}")
        else:
            print(f"  [FAIL] {diagram} - Failed to create")
