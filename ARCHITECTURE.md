# Architecture Documentation

## System Overview

The Career Readiness Mentor is built as an agentic AI system with a clear separation between reasoning agents, data retrieval, and user interface.

## Agentic Design

### Agent Responsibilities

Each agent has a specific role and uses the LLM as a reasoning engine:

1. **JD Parser Agent** (`agents/jd_parser.py`)
   - **Input**: Unstructured job description text
   - **Output**: Structured JSON with role, required/preferred skills, experience level
   - **Reasoning**: Uses LLM to extract and categorize skills from natural language

2. **Profile Analyzer Agent** (`agents/profile_analyzer.py`)
   - **Input**: Student profile (skills, degree, experience)
   - **Output**: Normalized skill categories, experience assessment
   - **Reasoning**: Normalizes skill names, categorizes into types

3. **Skill Gap Analyzer Agent** (`agents/skill_gap_analyzer.py`)
   - **Input**: Job skills + Student profile
   - **Output**: Missing/partial/strong skills with explanations
   - **Reasoning**: Compares skills, determines gaps, explains importance

4. **Roadmap Planner Agent** (`agents/roadmap_planner.py`)
   - **Input**: Skill gaps + Time constraints
   - **Output**: Week-by-week roadmap with milestones
   - **Reasoning**: Creates realistic learning sequence, considers dependencies

5. **Practice Generator Agent** (`agents/practice_generator.py`)
   - **Input**: Roadmap + Role + Skill gaps
   - **Output**: Coding challenges, interview questions, projects
   - **Reasoning**: Generates appropriate practice materials for skill level

6. **Reflection Agent** (`agents/reflection_agent.py`)
   - **Input**: Original roadmap + Progress data
   - **Output**: Updated recommendations, encouragement
   - **Reasoning**: Analyzes progress, identifies strengths/weaknesses, adjusts plan

## RAG Implementation

### Embedding Model
- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Why**: Lightweight, fast, suitable for hackathons
- **Usage**: Generates embeddings for semantic search

### Retrieval Process

1. **Course Retrieval** (`core/rag_service.py`)
   - Query: Skill name + Role
   - Embed all courses in database
   - Calculate cosine similarity
   - Return top K matches

2. **Job Description Retrieval**
   - Query: Role name
   - Embed all job descriptions
   - Find similar roles for context
   - Use for better skill extraction

### Data Flow

```
User Input (JD/Profile)
    ↓
Agent Processing (LLM)
    ↓
RAG Retrieval (Embeddings)
    ↓
LLM with Context
    ↓
Structured Output
```

## API Design

### RESTful Endpoints

All endpoints follow REST conventions:

- `POST /api/analyze-jd` - Create analysis
- `POST /api/analyze-profile` - Create profile analysis
- `POST /api/skill-gap` - Create gap analysis
- `POST /api/generate-roadmap` - Create roadmap
- `POST /api/generate-practice` - Create practice materials
- `POST /api/update-progress` - Update progress
- `GET /api/dashboard-summary` - Read summary

### Request/Response Format

All responses follow:
```json
{
  "success": true,
  "data": { ... }
}
```

Errors return HTTP status codes with:
```json
{
  "detail": "Error message"
}
```

## Database Schema

### Collections

1. **job_descriptions**
   ```json
   {
     "role": "Data Analyst",
     "description": "...",
     "skills": ["SQL", "Python"]
   }
   ```

2. **courses**
   ```json
   {
     "skill": "SQL",
     "resource_name": "SQL for Data Science",
     "provider": "Coursera",
     "url": "...",
     "description": "...",
     "difficulty": "beginner",
     "duration": "4 weeks"
   }
   ```

## Frontend Architecture

### Component Structure

```
App.jsx (Router)
├── Dashboard.jsx
├── Analysis.jsx
│   └── SkillGapChart.jsx
├── Roadmap.jsx
├── Practice.jsx
└── Progress.jsx
```

### State Management

- **Local State**: React hooks for component state
- **Persistence**: localStorage for cross-page data
- **API Calls**: Axios with centralized service (`services/api.js`)

### Data Flow

1. User input → Component state
2. API call → Backend agent
3. Response → Component state + localStorage
4. Navigation → Load from localStorage

## Security Considerations

1. **API Keys**: Stored in `.env`, never committed
2. **CORS**: Configured for localhost only
3. **Input Validation**: Pydantic models on backend
4. **No PII**: System doesn't store personal information
5. **Rate Limiting**: Consider adding for production

## Performance Optimizations

1. **Embedding Caching**: Consider caching computed embeddings
2. **Batch Processing**: Group similar queries
3. **Frontend Caching**: localStorage reduces API calls
4. **Lazy Loading**: Components load on demand

## Scalability Considerations

### Current Limitations
- Single MongoDB instance
- Synchronous LLM calls
- No caching layer

### Future Improvements
- Redis for caching
- Async task queue (Celery)
- Multiple MongoDB shards
- CDN for frontend assets

## Testing Strategy

### Unit Tests (Recommended)
- Test each agent independently
- Mock LLM responses
- Test RAG retrieval logic

### Integration Tests (Recommended)
- Test API endpoints
- Test data flow between agents
- Test frontend-backend integration

### Manual Testing
- Complete workflow end-to-end
- Test error handling
- Verify realistic outputs

## Deployment

### Backend
- FastAPI with Uvicorn
- Environment variables for config
- MongoDB connection pooling

### Frontend
- Vite build for production
- Static assets served via CDN
- Environment variables for API URL

### Recommended Stack
- **Backend**: Railway, Render, or AWS
- **Database**: MongoDB Atlas
- **Frontend**: Vercel, Netlify, or AWS S3+CloudFront
