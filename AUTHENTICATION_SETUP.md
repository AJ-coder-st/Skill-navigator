# Authentication & Email Setup Guide

## ✅ What's Been Added

### Backend
1. **User Authentication**
   - Register endpoint: `POST /api/auth/register`
   - Login endpoint: `POST /api/auth/login`
   - Get current user: `GET /api/auth/me`
   - JWT token-based authentication
   - Password hashing with bcrypt

2. **Email Service**
   - Sends analysis reports
   - Sends learning roadmaps
   - Sends milestone notifications
   - HTML email templates

3. **Email Integration**
   - Analysis reports sent automatically after skill gap analysis
   - Roadmaps sent automatically after generation
   - Milestone notifications (ready for implementation)

### Frontend
1. **Login Page** (`/login`)
   - Email and password login
   - Error handling
   - Redirects to dashboard on success

2. **Register Page** (`/register`)
   - Name, email, password registration
   - Password confirmation
   - Validation
   - Welcome email sent

3. **Navigation Updates**
   - Shows user name/email when logged in
   - Logout button
   - Login/Sign Up buttons when not logged in

4. **API Integration**
   - Automatic token attachment to requests
   - Token stored in localStorage

## 🔧 Configuration Required

### 1. Update `.env` File

Add these to `backend/.env`:

```env
# JWT Secret (use a random string in production)
JWT_SECRET_KEY=your-random-secret-key-here-change-in-production

# Email Settings (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
```

### 2. Gmail Setup (if using Gmail)

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification
   - Click "App passwords"
   - Generate a new app password for "Mail"
   - Use this password in `SMTP_PASSWORD`

### 3. Install Dependencies

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📧 Email Features

### Automatic Email Sending

1. **Analysis Report** - Sent after skill gap analysis
   - Includes job requirements
   - Your profile summary
   - Skill gaps breakdown
   - AI recommendations

2. **Learning Roadmap** - Sent after roadmap generation
   - Complete roadmap with milestones
   - Weekly breakdown
   - Skills to learn

3. **Milestone Notifications** - Ready for implementation
   - Sent when milestones are completed
   - Encouragement messages

## 🔐 How It Works

### Registration Flow
1. User fills registration form
2. Backend creates user account (hashed password)
3. JWT token generated
4. Welcome email sent
5. User redirected to dashboard

### Login Flow
1. User enters email/password
2. Backend verifies credentials
3. JWT token generated
4. Token stored in localStorage
5. User redirected to dashboard

### Protected Requests
- All API requests automatically include JWT token
- Backend validates token
- If valid, emails are sent automatically

## 🚀 Usage

### For Users
1. Go to `/register` to create account
2. Login at `/login`
3. Use the app normally
4. Reports and roadmaps will be emailed automatically

### Email Not Sent?
- Check `.env` file has correct SMTP settings
- Check backend console for email errors
- Email service will log errors but won't crash the app

## 📝 Notes

- **Email is optional**: App works without email configured (logs to console)
- **Tokens expire**: After 30 days, user needs to login again
- **Password security**: All passwords are hashed with bcrypt
- **No email verification**: Simple setup (can be added later)

## 🔒 Security Notes

- Change `JWT_SECRET_KEY` in production
- Use strong SMTP passwords
- Consider email verification for production
- Add rate limiting for login attempts
