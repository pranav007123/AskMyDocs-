# Admin Panel Setup Guide

## Overview

The Admin Panel allows administrators to:
- View system-wide analytics and statistics
- Manage all registered users
- Grant or revoke admin privileges
- Delete users and their data
- Monitor document uploads and activity

## Setup Instructions

### Step 1: Update Database Schema

If you have existing users, run the migration script to add the `is_admin` field:

```bash
python migrations/add_admin_field.py
```

This will add the `is_admin` column to the users table. All existing users will be set as regular users.

### Step 2: Make Your First Admin

#### Option A: Using the make_admin.py script

```bash
# Make a user admin by email
python make_admin.py admin@test.com

# List all users and their admin status
python make_admin.py list

# Revoke admin privileges
python make_admin.py revoke user@test.com
```

#### Option B: Using Python Console

```python
from app import app, db, User

with app.app_context():
    user = User.query.filter_by(email='admin@test.com').first()
    user.is_admin = True
    db.session.commit()
    print(f"✅ {user.username} is now an admin!")
```

#### Option C: Direct Database Update (SQLite)

```bash
sqlite3 instance/db.sqlite3
```

```sql
-- View all users
SELECT id, username, email, is_admin FROM users;

-- Make a user admin (replace email)
UPDATE users SET is_admin = 1 WHERE email = 'admin@test.com';

-- Verify
SELECT id, username, email, is_admin FROM users;

-- Exit
.quit
```

### Step 3: Access Admin Panel

1. Log in with an admin account
2. You'll see an "Admin" link in the navbar
3. Click it to access the Admin Dashboard

## Admin Features

### Admin Dashboard (`/admin`)

**Statistics Cards:**
- Total Users
- Total Documents
- Total Chunks
- Average Chunks per Document

**Analytics:**
- User activity (active vs inactive)
- Document type distribution
- Top users by document count

**Recent Activity:**
- Last 10 registered users
- Last 10 uploaded documents

### User Management (`/admin/users`)

**View All Users:**
- User ID, username, email
- Document and chunk counts
- Admin status badge
- Registration date

**Actions:**
- **Toggle Admin**: Grant or revoke admin privileges
- **Delete User**: Permanently delete user and all their data

**Safety Features:**
- Cannot modify your own admin status
- Cannot delete your own account
- Confirmation prompts for destructive actions

## Admin Permissions

### What Admins Can Do:
✅ View all users and their statistics  
✅ See system-wide analytics  
✅ Grant/revoke admin privileges to other users  
✅ Delete users and their documents  
✅ View all documents across the system  
✅ Access all regular user features  

### What Admins Cannot Do:
❌ Modify their own admin status  
❌ Delete their own account via admin panel  
❌ View actual document content without permission  
❌ Search other users' documents (privacy maintained)  

## Security Considerations

1. **Admin Decorator**: All admin routes are protected with `@admin_required` decorator
2. **Self-Protection**: Admins cannot remove their own privileges or delete themselves
3. **Confirmation**: Destructive actions require confirmation
4. **Audit Trail**: All admin actions are logged (timestamps in database)

## Database Schema Changes

### Added to User Model:
```python
is_admin = db.Column(db.Boolean, default=False, nullable=False)
```

This field:
- Defaults to `False` for new users
- Cannot be `NULL`
- Controls access to admin routes

## Troubleshooting

### Issue: "You do not have permission to access this page"

**Solution**: Your account is not an admin. Use `make_admin.py` to grant admin privileges.

```bash
python make_admin.py your@email.com
```

### Issue: Admin link not showing in navbar

**Solution**: 
1. Ensure you're logged in
2. Check your admin status: `python make_admin.py list`
3. Log out and log back in to refresh session

### Issue: Database migration fails

**Solution**: 
1. Backup your database: `cp instance/db.sqlite3 instance/db.sqlite3.backup`
2. Delete and recreate: `rm instance/db.sqlite3 && python run.py`
3. Or manually add column:
```sql
sqlite3 instance/db.sqlite3
ALTER TABLE users ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0;
.quit
```

### Issue: Cannot access admin panel after migration

**Solution**: Make sure you set at least one user as admin after migration:
```bash
python make_admin.py list  # View all users
python make_admin.py your@email.com  # Make yourself admin
```

## Testing the Admin Panel

### Create Test Users and Admin

```bash
# Start Python console
python

# Create test users
from app import app, db, User

with app.app_context():
    # Create regular user
    user1 = User(username='testuser', email='user@test.com')
    user1.set_password('test123')
    db.session.add(user1)
    
    # Create admin user
    admin = User(username='admin', email='admin@test.com')
    admin.set_password('admin123')
    admin.is_admin = True
    db.session.add(admin)
    
    db.session.commit()
    print("✅ Test users created!")
```

### Test Admin Features

1. Log in as `admin@test.com` / `admin123`
2. Navigate to `/admin`
3. Check analytics and statistics
4. Go to `/admin/users`
5. Try toggling admin status for `testuser`
6. Verify permissions work correctly

## Production Considerations

### Security Best Practices

1. **Strong Admin Passwords**: Enforce strong passwords for admin accounts
2. **Limit Admin Accounts**: Only create admin accounts for trusted users
3. **HTTPS Only**: Always use HTTPS in production
4. **Rate Limiting**: Add rate limiting to admin routes
5. **Audit Logging**: Log all admin actions to file/database

### Recommended Enhancements

```python
# Add to app.py for production

# 1. Admin action logging
import logging
admin_logger = logging.getLogger('admin_actions')

@app.route('/admin/user/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    user = User.query.get_or_404(user_id)
    admin_logger.info(f"Admin {current_user.username} deleted user {user.username}")
    # ... rest of code

# 2. Rate limiting (using Flask-Limiter)
from flask_limiter import Limiter

limiter = Limiter(app)

@app.route('/admin/users')
@limiter.limit("30 per minute")
@admin_required
def admin_users():
    # ... code
```

## Quick Reference Commands

```bash
# List all users
python make_admin.py list

# Make user admin
python make_admin.py user@example.com

# Revoke admin
python make_admin.py revoke user@example.com

# Run migration
python migrations/add_admin_field.py

# Check database
sqlite3 instance/db.sqlite3 "SELECT username, email, is_admin FROM users;"
```

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review Flask application logs
3. Check database integrity with `make_admin.py list`
4. Refer to main README.md for general setup issues
