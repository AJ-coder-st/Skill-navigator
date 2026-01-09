# Setup Guide

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=career_mentor
PORT=8000
EOF

# Get Gemini API key from: https://makersuite.google.com/app/apikey

# Start MongoDB (if local)
# macOS/Linux: brew services start mongodb-community
# Windows: Start MongoDB service

# Run backend
python main.py
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

### 3. Access the Application

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables

Create a `.env` file in the `backend/` directory with:

```
GEMINI_API_KEY=your_gemini_api_key_here
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=career_mentor
PORT=8000
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

## MongoDB Setup

### Option 1: Local MongoDB

1. Install MongoDB: https://www.mongodb.com/try/download/community
2. Start MongoDB service
3. Use `MONGODB_URI=mongodb://localhost:27017`

### Option 2: MongoDB Atlas (Cloud)

1. Create free account at https://www.mongodb.com/cloud/atlas
2. Create a cluster
3. Get connection string
4. Use `MONGODB_URI=your_atlas_connection_string`

## Troubleshooting

### Backend won't start
- Check MongoDB is running
- Verify `.env` file exists and has valid API key
- Check Python version (3.9+)

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify proxy in `frontend/vite.config.js`

### API errors
- Check Gemini API key is valid
- Get API key from: https://makersuite.google.com/app/apikey
- Verify API key has sufficient quota
- Check backend logs for detailed errors
