# Python Upgrade Instructions

## Current Issue
- Python 3.8.20 is installed (past EOL)
- google-generativeai requires Python 3.9+ (recommended: 3.10+)
- Warnings appear but code works with compatibility layer

## Option 1: Upgrade Python (Recommended)

### Windows Installation Steps:

1. **Download Python 3.10+ or 3.11+**
   - Visit: https://www.python.org/downloads/
   - Download Python 3.11.x (latest stable)
   - **IMPORTANT**: Check "Add Python to PATH" during installation

2. **Verify Installation**
   ```powershell
   python --version
   # Should show: Python 3.11.x
   ```

3. **Recreate Virtual Environment**
   ```powershell
   cd "D:\PROJECTS\Career Readiness Mentor & Skill-Gap Navigator\backend"
   Remove-Item -Recurse -Force venv
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Test Backend**
   ```powershell
   python main.py
   ```

## Option 2: Use Compatibility Layer (Current Fix)

The code has been updated to work with both old and new API versions.
Python 3.8 will work but with warnings. For production, upgrade to Python 3.10+.
