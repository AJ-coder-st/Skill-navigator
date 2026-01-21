# Career Readiness Mentor & Skill-Gap Navigator

An AI-powered platform that helps students and professionals identify skill gaps, analyze job requirements, and generate personalized learning roadmaps.

## 🎯 Features

- **Job Description Analysis**: AI-powered parsing of job descriptions to extract required skills
- **Resume Parsing & Matching**: Intelligent resume parsing from PDF/DOC/DOCX with accurate field extraction (name, email, experience) and Resume-JD matching with visual scorecards
- **Profile Analysis**: Normalize and analyze user skills and experience
- **Skill Gap Analysis**: Compare job requirements with user profile to identify gaps
- **Learning Roadmap**: Generate personalized 6-8 week learning plans
- **Practice Materials**: Get coding challenges, interview prep, and project ideas
- **Progress Tracking**: Monitor learning progress and get AI-powered recommendations
- **User Authentication**: Secure registration and login with JWT tokens
- **Email Notifications**: Automatic emails for analysis reports and roadmaps

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: MongoDB (MongoDB Atlas)
- **AI/ML**: 
  - Google Gemini API (LLM for reasoning and planning)
  - Sentence Transformers (Embeddings for RAG)
- **Authentication**: JWT tokens, bcr  ypt password hashing
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
├── backend/
│   ├── agents/          # AI agents (JD parser, profile analyzer, skill gap, roadmap, practice, reflection)
│   ├── api/             # API routes (auth, analysis endpoints)
│   ├── core/            # Core services (LLM, RAG, database, auth, email)
│   ├── data/            # Sample data (JDs, courses, challenges)
│   ├── main.py          # FastAPI application entry point
│   └── requirements.txt # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── services/    # API client
│   │   └── App.jsx      # Main app component
│   ├── package.json     # Node dependencies
│   └── vite.config.js    # Vite configuration
│
└── .env                  # Environment variables (not in git)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (3.10+ recommended)
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AJ-coder-st/Skill-navigator.git
   cd Skill-navigator
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the `backend` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   MONGODB_URI=your_mongodb_atlas_connection_string
   DATABASE_NAME=career_mentor
   PORT=8000
   
   JWT_SECRET_KEY=your-random-secret-key-here
   
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   FROM_EMAIL=your-email@gmail.com
   ```

5. **Run the Application**
   
   **Backend** (Terminal 1):
   ```bash
   cd backend
   venv\Scripts\activate  # Windows
   python main.py
   ```
   Backend runs on `http://localhost:8000`
   
   **Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (requires auth)

### Analysis
- `POST /api/analyze-jd` - Analyze job description (requires auth)
- `POST /api/analyze-profile` - Analyze user profile (requires auth)
- `POST /api/skill-gap` - Get skill gap analysis (requires auth)
- `POST /api/upload-resume` - Upload and parse resume (PDF/DOC/DOCX) (requires auth)
- `POST /api/match-resume-jd` - Match resume with job description and get visual scorecard (requires auth)

### Roadmap & Practice
- `POST /api/generate-roadmap` - Generate learning roadmap (requires auth)
- `POST /api/generate-practice` - Generate practice tasks (requires auth)
- `POST /api/update-progress` - Update learning progress (requires auth)
- `GET /api/dashboard-summary` - Get dashboard summary (requires auth)

## 🧠 AI Agents Architecture

The system uses multiple specialized AI agents:

1. **JD Parser Agent**: Extracts structured skill requirements from job descriptions
2. **Resume Analyzer Agent**: Multi-pass resume parsing with hallucination prevention, accurate name/email/experience extraction, and confidence tagging
3. **Profile Analyzer Agent**: Normalizes and analyzes user skills
4. **Skill Gap Analyzer Agent**: Identifies gaps and explains why skills matter
5. **Roadmap Planner Agent**: Generates realistic 6-8 week learning plans
6. **Practice Generator Agent**: Creates tailored practice tasks and challenges
7. **Reflection Agent**: Updates recommendations based on progress

## 📄 Resume Parsing Features

The Resume Analyzer uses a deterministic, multi-pass parsing pipeline:

- **Accurate Field Extraction**: 
  - Name extraction (excludes section headers like "EDUCATION", "EXPERIENCE")
  - Email validation (no inference or modification)
  - Experience calculation (handles Fresher, Not Mentioned, and year ranges)
  
- **Smart Experience Detection**:
  - Detects internships, trainees, and project-based experience
  - Returns "Fresher" for students/new graduates
  - Returns "Not Mentioned" when experience is unclear
  - Never defaults to "0 years"

- **Format Support**: PDF, DOC, DOCX with robust text cleaning and normalization

- **Resume-JD Matching**: 
  - Weighted scoring (40% core skills, 25% projects, 15% tools, 10% experience, 10% soft skills)
  - Skill classification (Strong, Partial, Weak/Missing)
  - Visual scorecards and charts for frontend rendering

## 🔐 Authentication

All analysis endpoints require authentication. Include the JWT token in the request header:

```
Authorization: Bearer <your_jwt_token>
```

## 📧 Email Notifications

The system automatically sends emails when:
- User registers (welcome email)
- Job description analysis completes
- Profile analysis completes
- Skill gap analysis completes
- Roadmap is generated
- Milestones are reached

Configure SMTP settings in `.env` to enable email notifications.

## 🎨 Frontend Features

- **Modern UI**: Clean, premium design with Tailwind CSS
- **AI Response Panels**: Structured, visually appealing AI output
- **Interactive Charts**: Skill gap visualization with Recharts
- **Responsive Design**: Works on all device sizes
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages

## 🧪 Testing

1. Register a new account or login
2. Navigate to Analysis page
3. Paste a job description and analyze
4. Enter your profile skills
5. View skill gap analysis
6. Generate a learning roadmap
7. Get practice tasks

## 📝 Sample Job Description

```
Software Engineer - Full Stack

We are looking for a Full Stack Software Engineer with 3+ years of experience.

Requirements:
- Strong proficiency in Python, JavaScript, and React
- Experience with FastAPI or Django
- Knowledge of MongoDB and SQL databases
- Familiarity with AWS cloud services
- Understanding of RESTful APIs
- Git version control

Preferred:
- Experience with Docker and Kubernetes
- Knowledge of CI/CD pipelines
- Agile/Scrum experience
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- **Repository**: https://github.com/AJ-coder-st/Skill-navigator
- **Backend API Docs**: http://localhost:8000/docs (when running)
- **Google Gemini API**: https://ai.google.dev/

## 💡 Notes

- The system uses Google Gemini API for LLM reasoning
- MongoDB Atlas is recommended for production
- Email service requires SMTP configuration
- All user data is stored securely in MongoDB
- The system includes fallback mechanisms if LLM is unavailable
