#!/bin/bash

# Backend startup script

echo "Starting Career Readiness Mentor Backend..."

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=career_mentor
PORT=8000
EOF
    echo "Please update .env with your OpenAI API key!"
fi

# Install dependencies if needed
if [ ! -d "venv/lib/python*/site-packages/fastapi" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Start the server
echo "Starting FastAPI server..."
python main.py
