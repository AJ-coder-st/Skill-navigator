@echo off
REM Backend startup script for Windows

echo Starting Career Readiness Mentor Backend...

cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    (
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo MONGODB_URI=mongodb://localhost:27017
        echo DATABASE_NAME=career_mentor
        echo PORT=8000
    ) > .env
    echo Please update .env with your OpenAI API key!
)

REM Install dependencies if needed
pip install -r requirements.txt

REM Start the server
echo Starting FastAPI server...
python main.py
