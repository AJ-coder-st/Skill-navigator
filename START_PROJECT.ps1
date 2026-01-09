# Quick Start Script - Starts both servers
# Usage: .\START_PROJECT.ps1

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Career Readiness Mentor" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$backendPath = Join-Path $scriptPath "backend"
$frontendPath = Join-Path $scriptPath "frontend"

# Start Backend
Write-Host "[1/2] Starting Backend Server..." -ForegroundColor Yellow
Set-Location $backendPath
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "  [ERROR] Virtual environment not found. Run .\setup.ps1 first" -ForegroundColor Red
    exit 1
}
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\venv\Scripts\Activate.ps1; Write-Host 'Backend Server - Port 8000' -ForegroundColor Green; python main.py" -WindowStyle Normal
Start-Sleep -Seconds 2

# Start Frontend
Write-Host "[2/2] Starting Frontend Server..." -ForegroundColor Yellow
Set-Location $frontendPath
if (-not (Test-Path "node_modules")) {
    Write-Host "  [ERROR] Dependencies not installed. Run .\setup.ps1 first" -ForegroundColor Red
    exit 1
}
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Frontend Server - Port 5173' -ForegroundColor Green; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Servers Starting..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Wait 10-15 seconds for servers to start," -ForegroundColor Yellow
Write-Host "then open http://localhost:5173 in your browser" -ForegroundColor Yellow
Write-Host ""

Set-Location $scriptPath
