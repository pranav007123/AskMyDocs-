from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

OUTPUT_FILE = "RAG_Project_Presentation.pdf"


def add_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(colors.grey)
    canvas.drawString(40, 20, "AskMyDocs - Retrieval-Augmented Generation with Flask")
    canvas.drawRightString(width - 40, 20, f"Page {doc.page}")
    canvas.restoreState()


def make_pdf(path: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='TitleBig', fontSize=20, leading=26, spaceAfter=16, alignment=1))
    styles.add(ParagraphStyle(name='H1', fontSize=16, leading=20, spaceBefore=10, spaceAfter=8, textColor=colors.HexColor('#0d6efd')))
    styles.add(ParagraphStyle(name='H2', fontSize=13, leading=18, spaceBefore=6, spaceAfter=6, textColor=colors.HexColor('#0b5ed7')))
    styles.add(ParagraphStyle(name='Body', fontSize=10.5, leading=15))
    styles.add(ParagraphStyle(name='BulletCustom', fontSize=10.5, leading=15, leftIndent=16, bulletIndent=8))
    styles.add(ParagraphStyle(name='Quote', fontSize=10.5, leading=16, leftIndent=12, textColor=colors.HexColor('#495057'), backColor=colors.whitesmoke))

    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=40, rightMargin=40, topMargin=50, bottomMargin=40)
    story = []

    # Cover
    story.append(Paragraph("AskMyDocs: Retrieval-Augmented Generation with Authentication", styles['TitleBig']))
    story.append(Paragraph("Presenter: Student | Technology: Flask, FAISS, Sentence-Transformers, Gemini/OpenAI", styles['Body']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Problem", styles['H1']))
    story.append(Paragraph("LLMs hallucinate and don't know your private documents. We need accurate answers grounded in user-provided content.", styles['Body']))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Solution Overview", styles['H1']))
    bullets = [
        "Upload PDFs/DOCX/TXT, extract text, chunk it (~500 tokens, 100 overlap)",
        "Embed chunks with all-MiniLM-L6-v2 (384-dim)",
        "Index per user in FAISS (cosine similarity via normalized inner product)",
        "On query: embed question → retrieve top-k → send context + question to LLM (Gemini/OpenAI)",
        "Return grounded answer + Source References"
    ]
    for b in bullets:
        story.append(Paragraph(f"• {b}", styles['BulletCustom']))

    story.append(PageBreak())

    # Architecture
    story.append(Paragraph("Architecture", styles['H1']))
    rows = [
        ["Component", "Technology"],
        ["Backend", "Flask + SQLAlchemy + Flask-Login"],
        ["Database", "SQLite (db.sqlite3)"],
        ["Embeddings", "Sentence-Transformers (all-MiniLM-L6-v2)"],
        ["Vector Store", "FAISS (per-user indexes)"],
        ["LLM Backend", "Gemini 1.5 Flash (default) or OpenAI GPT-4"],
        ["Document Parsing", "PyMuPDF (PDF), python-docx (DOCX), plain TXT"],
        ["UI", "Bootstrap 5 + custom CSS"],
    ]
    table = Table(rows, colWidths=[130, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.whitesmoke, colors.lightgrey]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(table)

    story.append(Spacer(1, 16))
    story.append(Paragraph("RAG Flow (Step-by-step)", styles['H1']))
    steps = [
        "Authenticate: Email + password (Flask-Login)",
        "Upload: Save file to /uploads, extract text",
        "Chunk: ~500 tokens with 100 overlap",
        "Embed: all-MiniLM-L6-v2 → 384-dim vectors",
        "Index: Add vectors + metadata to per-user FAISS index",
        "Query: Embed question, retrieve top-k similar chunks",
        "Generate: Prompt Gemini/OpenAI with query + retrieved chunks",
        "Display: Show answer + professional Source References"
    ]
    for s in steps:
        story.append(Paragraph(f"• {s}", styles['BulletCustom']))

    story.append(PageBreak())

    # Security & Isolation
    story.append(Paragraph("Security & Isolation", styles['H1']))
    points = [
        "Passwords hashed with Werkzeug; sessions managed by Flask-Login",
        "Per-user FAISS indexes in faiss_indexes/{user_id}/",
        "Users can only see their own documents and indexes",
        "File validation and 16MB limit; safe filenames",
        "API keys stored in .env (LLM_PROVIDER, GEMINI_API_KEY / OPENAI_API_KEY)"
    ]
    for p in points:
        story.append(Paragraph(f"• {p}", styles['BulletCustom']))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Key Routes & Functions (app.py)", styles['H1']))
    refs = [
        ("/register, /login, /logout", "User auth with email/password"),
        ("/dashboard", "Upload and list documents"),
        ("/upload", "Handle upload → extract → chunk → embed → index"),
        ("/search (GET/POST)", "Embed query → search FAISS → generate answer"),
        ("/download/<id>", "Download original file"),
        ("/delete_document/<id>", "Remove from FAISS + SQLite + uploads")
    ]
    for left, right in refs:
        story.append(Paragraph(f"<b>{left}</b>: {right}", styles['Body']))

    story.append(PageBreak())

    # Demo Script
    story.append(Paragraph("Demo Script (2–3 minutes)", styles['H1']))
    demo = [
        "Register a user → Login with email + password",
        "Upload a small TXT/PDF on Dashboard (show success + chunk count)",
        "Go to Search → Ask: 'What are the key features of this application?'",
        "Show AI Answer and professional Source References with relevance %"
    ]
    for d in demo:
        story.append(Paragraph(f"• {d}", styles['BulletCustom']))

    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))
    out_path = os.path.join(base_dir, OUTPUT_FILE)
    make_pdf(out_path)
    print(f"Generated: {out_path}")
