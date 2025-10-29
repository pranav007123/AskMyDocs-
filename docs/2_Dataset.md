# 2. DATASET SUMMARY

## 2.1 Description

**Type**: User-generated document corpus  
**Source**: User uploads via web interface  
**Formats**: PDF, DOCX, TXT  
**Max Size**: 16 MB per document

### Database Schema

**Users Table**
- id (PK), username, email, password_hash, created_at

**Documents Table**
- id (PK), user_id (FK), filename, original_name, file_type, uploaded_at, chunk_count

**FAISS Metadata** (per chunk)
- document_id, chunk_index, text, filename

**Embeddings**: 384-dimensional vectors (all-MiniLM-L6-v2)

## 2.2 Sample Data

### Documents Table (Sample)
| id | user_id | original_name | file_type | chunk_count |
|----|---------|---------------|-----------|-------------|
| 1 | 1 | research_paper.pdf | pdf | 64 |
| 2 | 1 | ml_notes.pdf | pdf | 82 |
| 3 | 2 | database_tutorial.pdf | pdf | 45 |

### Chunk Metadata (Sample)
```python
{
    'document_id': 1,
    'chunk_index': 0,
    'text': 'Introduction to Machine Learning...',
    'filename': 'research_paper.pdf'
}
```

## 2.3 Data Cleaning & Transformation

### 1. Text Extraction
- **PDF**: PyMuPDF extracts text from all pages
- **DOCX**: python-docx iterates paragraphs
- **TXT**: UTF-8 encoding with direct read

### 2. Text Chunking
```python
chunk_size = 500 tokens
overlap = 100 tokens
```
Overlapping preserves context across boundaries.

### 3. Embedding Generation
- Model: all-MiniLM-L6-v2
- Output: 384-dim vectors
- L2 normalized for cosine similarity

### 4. Validation
- File size limit (16MB)
- Extension validation (pdf, docx, txt)
- Empty text filtering
- Secure filename sanitization
