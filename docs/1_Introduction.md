# 1. INTRODUCTION

## 1.1 Problem Statement

In today's information-rich environment, organizations and individuals accumulate vast amounts of documents in various formats (PDFs, Word documents, text files). Finding relevant information presents several challenges:

- **Information Overload**: Manual searching through multiple documents is time-consuming
- **Context Loss**: Traditional keyword search fails to understand semantic meaning
- **Fragmented Knowledge**: Information scattered across multiple documents
- **No Intelligent Retrieval**: Cannot answer questions by synthesizing information from multiple sources
- **Security Concerns**: Lack of user-level access control and privacy

## 1.2 Proposed System

**AskMyDocs** is an intelligent document Q&A system using **Retrieval-Augmented Generation (RAG)**. The system combines semantic search with large language models to provide accurate, context-aware answers.

**Key Components:**
1. Document Processing Pipeline (PDF, DOCX, TXT)
2. Vector Database (FAISS) with 384-dimensional embeddings
3. Retrieval System using Sentence-Transformers
4. Generation System with OpenAI GPT-4 / Google Gemini
5. User Management with secure authentication

## 1.3 Features

- Multi-format document support (PDF, DOCX, TXT up to 16MB)
- Intelligent text chunking (500 tokens, 100 overlap)
- Semantic search with top-K retrieval
- AI-powered answers with source citations
- Semantic highlighting of relevant passages
- User authentication & per-user privacy
- Document management (upload, view, download, delete)
- Modern responsive UI with Bootstrap 5
- Flexible LLM backend (OpenAI/Gemini with auto-fallback)

## 1.4 Architecture Diagram

```
USER INTERFACE (Web App)
         ↓
FLASK APPLICATION
├─ Auth Routes (/register, /login, /logout)
├─ Upload Routes (/upload, /delete, /dashboard)
└─ Search Routes (/search)
         ↓
DATABASE LAYER (SQLite)
├─ User Model (id, username, email, password_hash)
└─ Document Model (id, user_id, filename, file_type, chunk_count)
         ↓
DOCUMENT PROCESSING
1. Text Extraction (PyMuPDF/python-docx)
2. Text Chunking (500 tokens, 100 overlap)
3. Embedding Generation (SentenceTransformer)
4. FAISS Indexing (per-user, 384-dim)
         ↓
RETRIEVAL SYSTEM
1. Query Embedding
2. FAISS Search (top-5)
3. Context Retrieval
4. Semantic Highlighting
         ↓
GENERATION SYSTEM
1. Prompt Building
2. LLM Generation (GPT-4/Gemini)
3. Answer Formatting
4. Fallback Handling
```
