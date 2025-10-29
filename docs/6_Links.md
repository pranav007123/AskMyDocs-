# 6. GITHUB REPOSITORY AND COLAB LINKS

## 6.1 URL of the GitHub Repository

**Repository URL**: `https://github.com/pranav007123/AskMyDocs-`

**Repository Structure:**
```
AskMyDocs/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── run.py                 # Application runner
├── init_db.py            # Database initialization
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── templates/            # HTML templates
│   ├── layout.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   └── search.html
├── static/
│   └── style.css         # Custom styles
├── docs/                 # Project documentation
│   ├── 1_Introduction.md
│   ├── 2_Dataset.md
│   ├── 3_Model_Building.md
│   ├── 4_Visualizations.md
│   ├── 5_Web_App.md
│   ├── 6_Links.md
│   ├── 7_Future.md
│   ├── 8_Conclusion.md
│   └── 9_References.md
├── uploads/              # User uploaded files
├── faiss_indexes/        # FAISS vector indexes
└── instance/
    └── db.sqlite3        # SQLite database
```

**Installation Instructions:**
```bash
# Clone repository
git clone https://github.com/pranav007123/AskMyDocs-.git
cd AskMyDocs-

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run application
python run.py
```

## 6.2 Colab Link

### Embedding Analysis Notebook
**URL**: `https://colab.research.google.com/drive/your-notebook-id`

**Notebook Contents:**
1. **Setup and Installation**
   - Install sentence-transformers
   - Install FAISS
   - Import required libraries

2. **Data Loading**
   - Load sample documents
   - Extract text from PDFs

3. **Embedding Generation**
   - Initialize all-MiniLM-L6-v2 model
   - Generate embeddings for text chunks
   - Visualize embedding dimensions

4. **Similarity Analysis**
   - Compute pairwise cosine similarity
   - Create similarity heatmaps
   - Identify semantic clusters

5. **FAISS Index Demo**
   - Build FAISS index
   - Perform sample searches
   - Measure query performance

6. **Visualization**
   - t-SNE dimensionality reduction
   - 2D embedding plots
   - Cluster analysis

### Performance Testing Notebook
**URL**: `https://colab.research.google.com/drive/your-perf-notebook-id`

**Notebook Contents:**
1. Load test documents
2. Benchmark embedding generation
3. Benchmark FAISS search
4. Compare different chunk sizes
5. Evaluate retrieval accuracy

### Sample Colab Code Snippet

```python
# Install dependencies
!pip install sentence-transformers faiss-cpu PyMuPDF

# Import libraries
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample documents
texts = [
    "Machine learning is a subset of AI...",
    "Supervised learning uses labeled data...",
    "Database normalization reduces redundancy...",
]

# Generate embeddings
embeddings = model.encode(texts)
print(f"Embedding shape: {embeddings.shape}")

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)

# Normalize and add
faiss.normalize_L2(embeddings)
index.add(embeddings)

# Search
query = "What is machine learning?"
query_vec = model.encode([query])
faiss.normalize_L2(query_vec)

scores, indices = index.search(query_vec, k=2)
print(f"Top results: {indices[0]}")
print(f"Scores: {scores[0]}")

# Visualize with t-SNE
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

plt.figure(figsize=(10, 6))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
for i, txt in enumerate(texts):
    plt.annotate(txt[:20], (embeddings_2d[i, 0], embeddings_2d[i, 1]))
plt.title('Document Embeddings (t-SNE)')
plt.show()
```
