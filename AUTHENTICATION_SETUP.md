# EDU_CHAT - User Authentication Setup Guide

## Overview
This document explains the new user authentication system implemented in EDU_CHAT. Each user can now register, login, and access only their own chat sessions.

## New Features
- **User Registration**: Users create an account with a username and password
- **User Login**: Session-based authentication 
- **User Isolation**: Each user only sees their own chat sessions
- **Auto-generated User ID**: 4 random digits generated for each user
- **Secure Password Hashing**: Passwords are hashed using werkzeug

## Database Changes

### New Table: `users`
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(4) UNIQUE NOT NULL,          -- 4-digit random ID
    username VARCHAR(50) UNIQUE NOT NULL,        -- Unique username
    password VARCHAR(255) NOT NULL,              -- Hashed password
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_username (username)
);
```

### Modified Table: `chat_sessions`
Added a new foreign key column:
```sql
ALTER TABLE chat_sessions ADD COLUMN user_id VARCHAR(4) AFTER id;
ALTER TABLE chat_sessions ADD CONSTRAINT fk_user_id 
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
CREATE INDEX idx_session_user_id ON chat_sessions(user_id);
```

**Important**: If you have existing chat_sessions in your database:
1. You must first create a test user (via registration)
2. OR convert your existing sessions (manual migration)
3. OR delete all existing sessions and start fresh

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

The new dependency added:
- `werkzeug==3.0.1` - For password hashing

### 2. Database Migration

#### Option A: Fresh Start (Recommended if no important data)
```bash
# Delete existing database and recreate
mysql -u root -p < database_creation.sql
mysql -u root -p < database_authentication_update.sql
```

#### Option B: Add to Existing Database
```bash
mysql -u root -p educhat_db < database_authentication_update.sql
```

Then manually migrate existing sessions (optional):
```sql
-- Create a temporary test user
INSERT INTO users (user_id, username, password) 
VALUES ('0000', 'admin', '<hashed_password>');

-- Update existing sessions (optional)
UPDATE chat_sessions SET user_id = '0000' WHERE user_id IS NULL;
```

### 3. Run the Application
```bash
python app.py
```

The app will start on `http://localhost:5000`

## How It Works

### Authentication Flow

#### Registration
1. User visits `http://localhost:5000/register`
2. Enters username (3-50 characters, alphanumeric + underscore only)
3. Creates password (minimum 6 characters)
4. System:
   - Validates inputs
   - Generates unique 4-digit user_id
   - Hashes password using werkzeug
   - Stores user in database
   - Returns user_id on success

#### Login
1. User visits `http://localhost:5000/login`
2. Enters username and password
3. System:
   - Looks up user by username
   - Verifies password hash
   - Stores userId in sessionStorage (client-side)
   - Redirects to chat page

#### Accessing Chat
- User is redirected to `/login` if not authenticated
- All API requests include `X-User-ID` header
- Backend validates user ownership of sessions
- User can only see their own chat history

### Session Management
- **Session Storage**: Uses browser `sessionStorage` (cleared when browser closes)
- **User ID Format**: Always sent in request headers as `X-User-ID`
- **Authentication Check**: All protected endpoints verify user exists and is valid

## API Endpoints

### Public Endpoints
- `POST /api/auth/register` - Register new user
  - Body: `{ username, password }`
  - Returns: `{ user_id, username, message }`
  
- `POST /api/auth/login` - Login user
  - Body: `{ username, password }`
  - Returns: `{ user_id, username, message }`

### Protected Endpoints (Require `X-User-ID` header)
- `GET /api/sessions` - Get user's chat sessions
- `GET /api/sessions/<id>` - Get specific session details
- `POST /api/chat` - Send chat message
- `DELETE /api/sessions/<id>` - Delete user's chat session

### Unprotected Endpoints
- `GET /api/classes` - List all classes
- `GET /api/subjects/<class_id>` - List subjects for a class

## Security Features

### Edge Cases Handled
1. **Duplicate Username**: Returns 409 (Conflict) error
2. **Invalid Credentials**: Returns 401 (Unauthorized) 
3. **Session Ownership**: Users can't access other users' sessions
4. **Unique User IDs**: 100-attempt retry to ensure uniqueness
5. **Password Requirements**: Minimum 6 characters, hashed with werkzeug
6. **Username Validation**: Only alphanumeric + underscore allowed
7. **Session Expiry**: Using sessionStorage (browser-managed expiration)
8. **CORS Protection**: Can be added to config if needed

## User Data Privacy
- Each user can ONLY access their own sessions
- Deleting a user cascades to delete all their sessions and messages
- Sessions include user_id in foreign key relationship
- Backend validates user_id on every request

## Client-Side Implementation
- **sessionStorage**: Stores userId and username
- **Auth Header**: Automatically added to all API requests
- **Auto-redirect**: Logged-out users redirected to login
- **Logout**: Clears sessionStorage and redirects to login

## Files Modified/Added

### New Files
- `templates/login.html` - Login form page
- `templates/register.html` - Registration form page  
- `static/auth-style.css` - Styling for auth pages
- `database_authentication_update.sql` - SQL migration script

### Modified Files
- `database.py` - Added User model
- `app.py` - Added auth endpoints and @require_auth decorator
- `templates/index.html` - Added auth checks, user info, logout button
- `static/style.css` - Added sidebar footer styling
- `requirements.txt` - Added werkzeug dependency

## Troubleshooting

### Issue: "Unauthorized" error on chat
**Solution**: User ID not being sent in headers. Check if sessionStorage has userId.

### Issue: "Session not found" when loading existing chat
**Solution**: User might be trying to access another user's session. Only your sessions will load.

### Issue: 500 error during registration
**Solution**: Check if users table exists. Run database SQL migration scripts.

### Issue: Password hashing errors
**Solution**: Ensure werkzeug is installed: `pip install werkzeug==3.0.1`

### Issue: Sessions disappear after browser close
**Solution**: This is expected behavior with sessionStorage. Users need to login again (this is by design for security).

## Future Enhancements
- JWT tokens instead of sessionStorage
- Email verification for registration
- Password reset functionality
- Remember me feature (httpOnly cookies)
- Rate limiting on auth endpoints
- Activity logging and audit trail
- Two-factor authentication (2FA)

## Notes
- User IDs are 4 random digits (0000-9999). Up to 10,000 unique users possible.
- For production, consider upgrading to a UUID system
- Passwords are hashed with werkzeug's strong hashing algorithm
- All timestamps are stored as UTC by default in MySQL

## Support
If you encounter issues:
1. Check database created users table
2. Verify werkzeug is installed
3. Check browser console for JavaScript errors
4. Review Flask app logs for backend errors
5. Ensure DATABASE_URL in .env is correct
