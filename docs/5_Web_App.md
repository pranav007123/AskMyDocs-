# 5. WEB APP INTEGRATION

## 5.1 Home Page

**URL**: `/` or `/index`

**Features:**
- Welcome message and project description
- "Get Started" button redirects to registration
- "Login" link for existing users
- Modern gradient UI with animations

**Technologies:**
- Bootstrap 5 responsive layout
- Custom CSS with gradients and shadows
- Font Awesome icons

## 5.2 Dashboards

### User Dashboard (`/dashboard`)

**Features:**
1. **Upload Section**
   - Drag-and-drop or click to upload
   - Real-time validation (file type, size)
   - Progress indicator
   - Success/error messages

2. **Document List Table**
   - Columns: Filename, Type, Uploaded Date, Chunks, Actions
   - Actions: Download, Delete
   - Sortable and responsive

3. **Statistics Cards**
   - Total documents count
   - Total chunks indexed
   - Storage used

**Access Control:**
- Requires authentication (@login_required)
- Shows only user's own documents
- User isolation enforced at database level

### Admin Features
Currently, no separate admin dashboard. All users have equal privileges with isolated data.

## 5.3 Other Pages

### Registration Page (`/register`)
**Fields:**
- Username (unique, required)
- Email (unique, validated)
- Password (hashed with Werkzeug)

**Validation:**
- Duplicate username/email checking
- Password strength (client-side)
- Form CSRF protection

### Login Page (`/login`)
**Fields:**
- Email
- Password

**Features:**
- "Remember me" checkbox
- Forgot password link (placeholder)
- Redirect to dashboard on success

### Search Page (`/search`)
**Components:**
1. **Search Bar**
   - Natural language query input
   - Document filter dropdown (all or specific)
   - Search button with loading indicator

2. **Results Section**
   - AI-generated answer card (with emoji indicator)
   - Source chunks with semantic highlighting
   - Similarity scores display
   - Expandable/collapsible chunks

3. **No Results Handling**
   - Friendly message
   - Suggestions to rephrase
   - Link to upload more documents

## 5.4 Demo Usernames and Passwords

### Test Accounts

**User 1:**
```
Email: user1@test.com
Password: test123
Documents: 2 PDFs (ML-related)
```

**User 2:**
```
Email: user2@test.com
Password: test123
Documents: 2 PDFs (Database/Python)
```

**User 3:**
```
Email: admin@test.com
Password: admin123
Documents: 1 PDF (Web Development)
```

**User 4:**
```
Email: demo@test.com
Password: demo123
Documents: 1 PDF (Project Docs)
```

### Creating New Test Account

```bash
# Via Python console
from app import app, db, User

with app.app_context():
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
```

## 5.5 UI/UX Features

**Design System:**
- Primary gradient: Purple to violet (#667eea → #764ba2)
- Success gradient: Blue to cyan (#4facfe → #00f2fe)
- Card-based layouts with soft shadows
- Smooth hover animations and transitions

**Responsive Design:**
- Mobile-first approach
- Breakpoints for tablet and desktop
- Touch-friendly buttons and forms

**Accessibility:**
- Semantic HTML5
- ARIA labels on interactive elements
- Keyboard navigation support
- High contrast text
