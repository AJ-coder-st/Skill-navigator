# Career Readiness Mentor & Skill-Gap Navigator

An AI-powered platform that helps students and professionals identify skill gaps, analyze job requirements, and generate personalized learning roadmaps.

## 🎯 Features

### Core Functionality
- **Job Description Analysis**: AI-powered parsing of job descriptions to extract required skills
- **Profile Analysis**: Normalize and analyze user skills and experience
- **Skill Gap Analysis**: Compare job requirements with user profile to identify gaps
- **Learning Roadmap**: Generate personalized 6-8 week learning plans
- **Practice Materials**: Get coding challenges, interview prep, and project ideas
- **Progress Tracking**: Monitor learning progress and get AI-powered recommendations

### User Features
- **User Authentication**: Register and login with email/password
- **Email Notifications**: Automatic emails for analysis reports, roadmaps, and milestones
- **Premium UI**: Beautiful, structured AI response panels
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: MongoDB (MongoDB Atlas)
- **AI/ML**: 
  - Google Gemini API (LLM)
  - Sentence Transformers (Embeddings for RAG)
- **Authentication**: JWT tokens, bcrypt password hashing
- **Email**: SMTP (aiosmtplib)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **Icons**: Lucide React
- **Routing**: React Router DOM

## 📁 Project Structure

```
Career Readiness Mentor & Skill-Gap Navigator/
├── backend/
│   ├── agents/          # AI agents (JD parser, profile analyzer, etc.)
│   ├── api/             # API routes (auth, analysis endpoints)
│   ├── core/            # Core services (LLM, RAG, database, auth, email)
│   ├── data/            # Sample data (JDs, courses, challenges)
│   ├── main.py          # FastAPI application entry point
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API service layer
│   │   └── App.jsx      # Main app component
│   └── package.json     # Node dependencies
├── manage_project.bat   # Windows project manager
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (3.11 recommended)
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Google Gemini API key

### Backend Setup

1. **Navigate to backend directory**:
   ```powershell
   cd backend
   ```

2. **Create virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create `backend/.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
   DATABASE_NAME=career_mentor
   PORT=8000
   JWT_SECRET_KEY=your-random-secret-key
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   ```

5. **Start backend server**:
   ```powershell
   python main.py
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```powershell
   cd frontend
   ```

2. **Install dependencies**:
   ```powershell
   npm install
   ```

3. **Start development server**:
   ```powershell
   npm run dev
   ```

### Using the Project Manager (Windows)

Run `manage_project.bat` for an interactive menu to:
- Start/stop backend and frontend servers
- Restart servers
- Check server status

## 📧 Email Configuration

### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Google Account → Security → 2-Step Verification → App passwords
   - Use the generated password in `SMTP_PASSWORD`

### Email Features
- **Welcome Email**: Sent on registration
- **Analysis Reports**: Sent after skill gap analysis
- **Learning Roadmaps**: Sent after roadmap generation
- **Milestone Notifications**: Ready for implementation

## 🔐 Authentication

### Endpoints
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Features
- JWT token-based authentication (30-day expiry)
- Password hashing with bcrypt
- Email validation
- Password length validation (6-72 characters)

## 📊 API Endpoints

### Analysis
- `POST /api/analyze-jd` - Analyze job description
- `POST /api/analyze-profile` - Analyze user profile
- `POST /api/skill-gap` - Analyze skill gaps

### Roadmap & Practice
- `POST /api/generate-roadmap` - Generate learning roadmap
- `POST /api/generate-practice` - Generate practice materials
- `POST /api/update-progress` - Update learning progress

### Dashboard
- `GET /api/dashboard-summary` - Get dashboard statistics

## 🎨 UI Features

- **Premium AI Response Panels**: Structured, easy-to-scan results
- **Skill Cards**: Color-coded (strong/partial/missing)
- **Match Score**: Visual progress bar
- **Loading Skeletons**: Professional loading states
- **Accordion Sections**: Collapsible long content
- **Responsive Design**: Mobile-friendly

## 🔧 Configuration

### Backend Configuration
Edit `backend/core/config.py` or use environment variables:
- `LLM_MODEL`: Gemini model (default: gemini-1.5-flash)
- `EMBEDDING_MODEL`: Sentence transformer model
- `TOP_K_RESULTS`: Number of RAG results

### Frontend Configuration
Edit `frontend/src/services/api.js`:
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000/api)

## 📝 Sample Data

Sample job descriptions and courses are included in:
- `backend/data/sample_job_descriptions.json`
- `backend/data/sample_courses.json`
- `SAMPLE_JD.txt`, `SAMPLE_JD_2.txt`, `SAMPLE_JD_3.txt`

## 🐛 Troubleshooting

### Backend Issues
- **Import Errors**: Ensure all dependencies are installed
- **MongoDB Connection**: Check `MONGODB_URI` in `.env`
- **Gemini API Errors**: Verify `GEMINI_API_KEY` is correct
- **Python 3.8 Warnings**: Non-fatal, upgrade to Python 3.11 to remove

### Frontend Issues
- **White Screen**: Check browser console for errors
- **API Connection**: Verify backend is running on port 8000
- **Build Errors**: Run `npm install` to ensure dependencies are installed

## 📚 Documentation

- `ARCHITECTURE.md` - System architecture details
- `AUTHENTICATION_SETUP.md` - Auth and email setup guide
- `FINAL_PRODUCTION_FIX.md` - Production fixes applied
- `FRONTEND_UI_REDESIGN.md` - UI improvements documentation

## 🎯 Future Enhancements

- Email verification
- Password reset functionality
- Social login (Google, GitHub)
- Advanced progress analytics
- Export reports as PDF
- Dark mode
- Multi-language support

## 📄 License

This project is part of a hackathon submission.

## 👥 Contributors

Built for Career Readiness and Skill Development.

---

**Status**: ✅ Production Ready
