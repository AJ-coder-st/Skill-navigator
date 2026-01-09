# Career Readiness Mentor - One-Click Setup Script
# Run this script to set up the entire project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Career Readiness Mentor Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/4] Checking Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Python not found. Please install Python 3.10+ from python.org" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] $pythonVersion" -ForegroundColor Green

# Check Node.js
Write-Host "[2/4] Checking Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [ERROR] Node.js not found. Please install Node.js from nodejs.org" -ForegroundColor Red
    exit 1
}
Write-Host "  [OK] Node.js $nodeVersion" -ForegroundColor Green

# Setup Backend
Write-Host "[3/4] Setting up Backend..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot "backend"
Set-Location $backendPath

if (Test-Path "venv") {
    Write-Host "  Removing old virtual environment..." -ForegroundColor Gray
    Remove-Item -Recurse -Force venv
}

Write-Host "  Creating virtual environment..." -ForegroundColor Gray
python -m venv venv

Write-Host "  Activating virtual environment..." -ForegroundColor Gray
& ".\venv\Scripts\Activate.ps1"

Write-Host "  Upgrading pip..." -ForegroundColor Gray
python -m pip install --upgrade pip -q

Write-Host "  Installing dependencies..." -ForegroundColor Gray
pip install -r requirements.txt -q

Write-Host "  [OK] Backend setup complete" -ForegroundColor Green

# Setup Frontend
Write-Host "[4/4] Setting up Frontend..." -ForegroundColor Yellow
$frontendPath = Join-Path $PSScriptRoot "frontend"
Set-Location $frontendPath

if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing dependencies..." -ForegroundColor Gray
    npm install
} else {
    Write-Host "  Dependencies already installed" -ForegroundColor Gray
}

Write-Host "  [OK] Frontend setup complete" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the project, run:" -ForegroundColor Yellow
Write-Host "  .\manage_project.bat" -ForegroundColor White
Write-Host ""
Write-Host "Or start manually:" -ForegroundColor Yellow
Write-Host "  Backend:  cd backend && .\venv\Scripts\Activate.ps1 && python main.py" -ForegroundColor White
Write-Host "  Frontend: cd frontend && npm run dev" -ForegroundColor White
Write-Host ""

Set-Location $PSScriptRoot
