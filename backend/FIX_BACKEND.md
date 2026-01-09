# Backend Fix Commands

## Step 1: Upgrade google-generativeai (if Python 3.10+)

```powershell
cd "D:\PROJECTS\Career Readiness Mentor & Skill-Gap Navigator\backend"
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip uninstall google-generativeai -y
pip install google-generativeai>=0.3.0
```

## Step 2: Reinstall All Dependencies (Recommended)

```powershell
cd "D:\PROJECTS\Career Readiness Mentor & Skill-Gap Navigator\backend"
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 3: Test Backend

```powershell
python main.py
```

Expected output:
```
Connected to MongoDB: career_mentor
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 4: Test API

```powershell
# In another terminal
Invoke-WebRequest -Uri http://localhost:8000/health
```

Expected: `{"status":"healthy"}`
