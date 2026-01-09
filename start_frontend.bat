@echo off
REM Frontend startup script for Windows

echo Starting Career Readiness Mentor Frontend...

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Start the dev server
echo Starting Vite dev server...
call npm run dev
