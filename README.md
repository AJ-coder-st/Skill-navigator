# Career Readiness Mentor & Skill-Gap Navigator

An AI-powered system that helps students map job descriptions to their current skills, identify skill gaps, and generate realistic, milestone-based upskilling roadmaps with practice tasks and progress tracking.

## 🎯 Project Overview

This hackathon-ready project provides an agentic AI system that acts as a **reasoning and planning engine** (not a chatbot) to:

1. Parse unstructured job descriptions into structured skill requirements
2. Compare extracted skills with student profiles
3. Reason about skill gaps and explain why each skill matters
4. Generate realistic 6–8 week learning roadmaps
5. Generate tailored practice materials (coding challenges, behavioral interview prompts, mini-projects)
6. Reflect on progress and update recommendations using memory

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- React 18 with Vite
- Tailwind CSS for styling
- Recharts for data visualization
- React Router for navigation

**Backend:**
- Python 3.9+
- FastAPI for REST APIs
- MongoDB for data storage
- Motor (async MongoDB driver)

**AI/ML:**
- OpenAI GPT-4/GPT-3.5 (or compatible API)
- sentence-transformers (all-MiniLM-L6-v2) for embeddings
- RAG (Retrieval-Augmented Generation) for course recommendations

### Agentic Architecture

The system is designed as multiple logical agents:

1. **JD Parser Agent** - Extracts structured skills from job descriptions
2. **Profile Analyzer Agent** - Normalizes and categorizes student skills
3. **Skill Gap Reasoning Agent** - Identifies missing/partial/strong skills with explanations
4. **Roadmap Planner Agent** - Generates week-by-week learning roadmaps
5. **Practice Generator Agent** - Creates coding challenges, behavioral questions, and mini-projects
6. **Reflection Agent** - Analyzes progress and updates recommendations

### RAG Implementation

- Stores job description samples and course catalog embeddings
- Retrieves relevant documents based on role/skills using semantic search
- Passes retrieved content to LLM for grounded responses
- Cites sources in output (no hallucinated courses)

## 📁 Project Structure

```
.
├── backend/
│   ├── agents/              # AI agent implementations
│   │   ├── jd_parser.py
│   │   ├── profile_analyzer.py
│   │   ├── skill_gap_analyzer.py
│   │   ├── roadmap_planner.py
│   │   ├── practice_generator.py
│   │   └── reflection_agent.py
│   ├── api/
│   │   └── routes.py        # FastAPI endpoints
│   ├── core/
│   │   ├── config.py        # Configuration settings
│   │   ├── database.py      # MongoDB connection
│   │   ├── llm_service.py   # LLM integration
│   │   └── rag_service.py   # RAG implementation
│   ├── data/
│   │   ├── sample_job_descriptions.json
│   │   ├── sample_courses.json
│   │   └── coding_challenges.json
│   ├── main.py              # FastAPI app entry point
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Analysis.jsx
│   │   │   ├── Roadmap.jsx
│   │   │   ├── Practice.jsx
│   │   │   ├── Progress.jsx
│   │   │   └── SkillGapChart.jsx
│   │   ├── services/
│   │   │   └── api.js       # API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- MongoDB (local or cloud instance)
- Google Gemini API key (get from https://makersuite.google.com/app/apikey)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=career_mentor
PORT=8000
```

   Get your Gemini API key from: https://makersuite.google.com/app/apikey

5. Start MongoDB (if running locally):
```bash
# On macOS/Linux with Homebrew:
brew services start mongodb-community

# On Windows, start MongoDB service or run:
mongod
```

6. Run the FastAPI server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📡 API Endpoints

### POST `/api/analyze-jd`
Analyzes a job description and extracts structured skill requirements.

**Request:**
```json
{
  "job_description": "Full job description text..."
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "role": "Data Analyst",
    "required_skills": ["SQL", "Python", "Statistics"],
    "preferred_skills": ["Machine Learning"],
    "experience_level": "mid",
    "reasoning": "..."
  }
}
```

### POST `/api/analyze-profile`
Analyzes and normalizes a student profile.

**Request:**
```json
{
  "degree": "B.Tech IT",
  "skills": ["Python", "JavaScript"],
  "experience_level": "beginner",
  "projects": ["Todo App"],
  "certifications": []
}
```

### POST `/api/skill-gap`
Analyzes skill gaps between job requirements and student profile.

### POST `/api/generate-roadmap`
Generates a learning roadmap based on skill gaps.

### POST `/api/generate-practice`
Generates practice materials (coding challenges, interview questions, projects).

### POST `/api/update-progress`
Reflects on student progress and provides updated recommendations.

### GET `/api/dashboard-summary`
Returns dashboard statistics.

## 🎨 Frontend Features

### Dashboard
- System status overview
- Quick statistics
- Getting started guide

### Analysis Page
- Job description input and analysis
- Student profile input and normalization
- Skill gap visualization with charts
- AI reasoning explanations

### Roadmap Page
- Week-by-week learning roadmap
- Milestones and checkpoints
- Learning objectives
- Practice tasks per week

### Practice Page
- Coding challenges (beginner/intermediate/advanced)
- Behavioral interview questions
- Mini-project ideas
- Difficulty levels and time estimates

### Progress Page
- Progress tracking interface
- AI-powered reflection and recommendations
- Updated roadmap suggestions
- Encouragement and next steps

## 🔄 User Workflow

The application follows a sequential workflow:

1. **Analysis** → Paste job description and enter your profile
   - System extracts skills from JD
   - Normalizes your profile
   - Identifies skill gaps

2. **Roadmap** → Generate learning roadmap
   - Set timeline (4-12 weeks)
   - Get week-by-week plan with milestones

3. **Practice** → Get practice materials
   - Coding challenges
   - Interview questions
   - Mini-projects

4. **Progress** → Track and reflect
   - Update completed milestones
   - Get AI-powered reflection
   - Receive updated recommendations

**Note**: Data flows between pages via localStorage. Complete Analysis before Roadmap, etc.

## 🔧 Configuration

### LLM Model Selection

The system uses Google Gemini Pro by default. To use a different Gemini model:

1. Update `backend/core/config.py`:
```python
LLM_MODEL = "gemini-pro"  # or "gemini-pro-vision" for vision tasks
```

2. For other LLM providers, modify `backend/core/llm_service.py` to use your preferred API.

### Database

The system uses MongoDB by default. Sample data is automatically loaded on first run if collections are empty.

To use SQLite instead:
1. Modify `backend/core/database.py` to use SQLite
2. Update connection logic accordingly

## 📊 Data Sources

### Sample Datasets

The project includes sample data in `backend/data/`:

- **sample_job_descriptions.json** - 8 sample job descriptions across different roles
- **sample_courses.json** - 15 curated course recommendations from public sources
- **coding_challenges.json** - Template coding challenges

### Data Ethics

- ✅ Uses only public or synthetic data
- ✅ No scraping of restricted platforms
- ✅ No PII storage
- ✅ No fake credentials or certifications
- ✅ All course recommendations are from legitimate public sources

## 🧪 Evaluation Criteria

The system is designed to meet hackathon evaluation criteria:

- **Accuracy**: Structured skill extraction, realistic gap analysis
- **Feasibility**: Realistic timelines (no "learn ML in 1 week")
- **Explainability**: Clear AI reasoning for all decisions
- **User Experience**: Clean, intuitive interface with clear workflows

## 🚨 Important Notes

1. **API Key Required**: You must provide a valid OpenAI API key in the `.env` file
2. **MongoDB**: Ensure MongoDB is running before starting the backend
3. **Realistic Timelines**: The system enforces realistic learning timelines
4. **No Hallucinations**: RAG ensures course recommendations are grounded in real data

## 🐛 Troubleshooting

### Backend Issues

**Error: "Gemini API key not configured"**
- Ensure `.env` file exists with `GEMINI_API_KEY` set
- Get your API key from: https://makersuite.google.com/app/apikey

**Error: "Failed to connect to MongoDB"**
- Check MongoDB is running: `mongosh` or check service status
- Verify `MONGODB_URI` in `.env` is correct

### Frontend Issues

**Error: "Network Error" or CORS issues**
- Ensure backend is running on port 8000
- Check `vite.config.js` proxy configuration

**Components not loading data**
- Check browser console for errors
- Verify API endpoints are accessible
- Check localStorage for saved data

## 📝 License

This project is created for hackathon purposes. Use responsibly and in accordance with OpenAI's usage policies.

## 🤝 Contributing

This is a hackathon project. For improvements:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Support

For issues or questions:
- Check the troubleshooting section
- Review API documentation at `http://localhost:8000/docs` (FastAPI auto-generated docs)
- Check browser console and backend logs

---

**Built for Hackathon 2024** | Career Readiness Mentor & Skill-Gap Navigator
