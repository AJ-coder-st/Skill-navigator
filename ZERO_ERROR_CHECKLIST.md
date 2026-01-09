# Zero-Error Verification Checklist

## ✅ Pre-Startup Checks

### Backend
- [ ] Python 3.10+ installed (or 3.8 with compatibility layer)
- [ ] Virtual environment created: `backend/venv/`
- [ ] All dependencies installed: `pip list` shows all packages
- [ ] `.env` file exists with `GEMINI_API_KEY` and `MONGODB_URI`
- [ ] MongoDB accessible (local or Atlas)

### Frontend
- [ ] Node.js 18+ installed
- [ ] `node_modules/` directory exists
- [ ] Vite installed: `npm list vite`
- [ ] All dependencies installed: `npm list`

## ✅ Startup Verification

### Backend Startup
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

**Expected Output (No Errors):**
```
Connected to MongoDB: career_mentor
Loaded X sample job descriptions
Loaded X sample courses
INFO:     Started server process [XXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**No Errors Should Appear:**
- ❌ No `AttributeError: 'GenerativeModel'`
- ❌ No `ModuleNotFoundError`
- ❌ No `ConnectionError` (unless MongoDB is actually down)
- ⚠️  Warnings about Python 3.8 are OK (but upgrade recommended)

### Frontend Startup
```powershell
cd frontend
npm run dev
```

**Expected Output (No Errors):**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**No Errors Should Appear:**
- ❌ No `'Skill-Gap' is not recognized`
- ❌ No `Cannot find module 'vite'`
- ❌ No `ENOENT` errors
- ❌ No path parsing errors

## ✅ Runtime Verification

### Backend API Test
```powershell
Invoke-WebRequest -Uri http://localhost:8000/health
```

**Expected:** `{"status":"healthy"}`

### Frontend Access
Open browser: `http://localhost:5173`

**Expected:**
- Page loads without errors
- No console errors in browser DevTools
- API calls work (check Network tab)

## ✅ Error Resolution

### If Backend Fails:
1. Check Python version: `python --version`
2. Verify venv activation: `where python` (should point to venv)
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
4. Check `.env` file exists and has correct values
5. Test MongoDB connection separately

### If Frontend Fails:
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` fresh
3. Verify Vite: `npm list vite`
4. Check for path issues in terminal output
5. Try `npx vite` directly

## ✅ Final Success Criteria

After all fixes:
- ✅ `python main.py` starts without errors
- ✅ `npm run dev` starts without errors
- ✅ Both servers accessible via browser
- ✅ No fatal warnings (Python 3.8 warnings are acceptable but not ideal)
- ✅ API endpoints respond correctly
- ✅ Frontend loads and makes API calls successfully
