# Python Upgrade Guide

## Current Issue
- Python 3.8.20 is End of Life (EOL since October 2024)
- Causes FutureWarning messages
- May have compatibility issues with latest packages

## Recommended: Upgrade to Python 3.11

### Step 1: Download Python 3.11
1. Visit: https://www.python.org/downloads/
2. Download Python 3.11.x (latest stable)
3. **IMPORTANT**: During installation, check "Add Python to PATH"

### Step 2: Verify Installation
```powershell
python --version
# Should show: Python 3.11.x
```

### Step 3: Recreate Virtual Environment
```powershell
cd "D:\PROJECTS\Career Readiness Mentor & Skill-Gap Navigator\backend"

# Remove old venv
Remove-Item -Recurse -Force venv

# Create new venv with Python 3.11
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Verify No Warnings
```powershell
python main.py
# Should start without FutureWarning messages
```

## Alternative: Keep Python 3.8 (Not Recommended)

The code will work with Python 3.8, but you'll see warnings. For production, upgrade to Python 3.10+.
