# AskMyDocs - RAG Flask Application

A complete Flask application that implements Retrieval-Augmented Generation (RAG) with user authentication. Users can register, upload documents (PDF, DOCX, TXT), and ask questions that are answered using embeddings and GPT-4.

## Features

- **User Authentication**: Register, login, logout with Flask-Login
- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Text Processing**: Automatic text extraction and chunking
- **Vector Search**: FAISS-based similarity search with sentence transformers
- **AI Responses**: GPT-4 powered answers with source citations
- **Document Management**: View, download, and delete uploaded documents
- **Modern UI**: Bootstrap-styled responsive interface

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Authentication**: Flask-Login with password hashing
- **Database**: SQLite
- **Vector Storage**: FAISS
- **Embeddings**: Sentence-Transformers (all-MiniLM-L6-v2)
- **LLM**: OpenAI GPT-4
- **Document Processing**: PyMuPDF (PDF), python-docx (DOCX)
- **Frontend**: Bootstrap 5, Font Awesome

## Project Structure

```
askmydocs/
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy database models
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── README.md             # This file
├── db.sqlite3            # SQLite database (created automatically)
├── uploads/              # Uploaded files storage
├── faiss_indexes/        # FAISS indexes per user
└── templates/            # HTML templates
    ├── layout.html       # Base template
    ├── index.html        # Home page
    ├── register.html     # User registration
    ├── login.html        # User login
    ├── dashboard.html    # Document management
    └── search.html       # Search interface
```

## Setup Instructions

### 1. Clone and Navigate

```bash
cd "d:\marian 3rd sem\AskMyDocs"
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here_change_this_in_production
```

**Important**: 
- Get your OpenAI API key from https://platform.openai.com/api-keys
- Generate a secure secret key for production use

### 5. Initialize Database

The database will be created automatically when you first run the app. The SQLite file `db.sqlite3` will be created in the project root.

Optional: If you prefer Flask-Migrate, you can initialize migrations (not required for this project):

```bash
set FLASK_APP=app.py  # Windows PowerShell: $env:FLASK_APP="app.py"
flask db init
flask db migrate -m "init"
flask db upgrade
```

### 6. Run the Application

```bash
python app.py
```

The application will be available at: http://localhost:5000

## Usage Guide

### 1. Register an Account
- Go to http://localhost:5000
- Click "Create Account"
- Fill in username, email, and password
- Click "Create Account"

### 2. Upload Documents
- After logging in, you'll see the Dashboard
- Use the upload form to select PDF, DOCX, or TXT files
- Click "Upload Document"
- The system will extract text and create embeddings

### 3. Search Documents
- Go to the "Search" page
- Enter your question in natural language
- Choose to search all documents or a specific one
- Click "Search" to get AI-powered answers

### 4. Manage Documents
- View all uploaded documents on the Dashboard
- Download original files
- Delete documents (removes from database and search index)

## API Endpoints

- `GET /` - Home page
- `GET,POST /register` - User registration
- `GET,POST /login` - User login
- `GET /logout` - User logout
- `GET /dashboard` - Document management dashboard
- `POST /upload` - File upload
- `GET /delete_document/<id>` - Delete document
- `GET /download/<id>` - Download document
- `GET,POST /search` - Search interface and processing

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `created_at`

### Documents Table
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `filename` (Stored filename)
- `original_name` (Original filename)
- `file_type` (pdf, docx, txt)
- `uploaded_at`
- `chunk_count`

## Configuration

### File Upload Limits
- Maximum file size: 16MB
- Supported formats: PDF, DOCX, TXT

### Text Processing
- Chunk size: 500 tokens
- Chunk overlap: 100 tokens
- Embedding model: all-MiniLM-L6-v2 (384 dimensions)

### Search Parameters
- Default retrieval: Top 5 most similar chunks
- Similarity metric: Cosine similarity (Inner Product in FAISS)
- LLM: GPT-4 with 500 max tokens

## Security Features

- Password hashing with Werkzeug
- User session management with Flask-Login
- File type validation
- User isolation (users only see their own documents)
- Secure filename handling

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure your API key is correctly set in `.env`
   - Check that you have sufficient credits in your OpenAI account

2. **File Upload Issues**
   - Check file size (max 16MB)
   - Ensure file format is supported (PDF, DOCX, TXT)
   - Verify the `uploads/` directory exists and is writable

3. **Database Issues**
   - Delete `rag_app.db` to reset the database
   - Check file permissions in the project directory

4. **FAISS Index Issues**
   - Delete the `faiss_indexes/` directory to reset all indexes
   - Ensure sufficient disk space for embeddings storage

### Performance Notes

- First-time model loading (sentence-transformers) may take a few minutes
- Large documents will take longer to process
- FAISS indexes grow with the number of uploaded documents

## Development

### Adding New Features

1. **New File Types**: Extend `extract_text_from_file()` function
2. **Different Embeddings**: Change the model in `embedding_model` initialization
3. **Custom Chunking**: Modify `chunk_text()` function
4. **UI Improvements**: Edit templates in `templates/` directory

### Testing

Test the application with various document types and queries to ensure proper functionality.

## License

This project is for educational purposes. Please ensure you comply with OpenAI's usage policies when using their API.

## Support

For issues or questions, please check the troubleshooting section above or review the code comments for implementation details.
