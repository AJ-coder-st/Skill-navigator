# Verification Steps - Post Fix

## Step 1: Verify Package Upgrade

```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip show google-generativeai
```

**Expected**: Version should be >= 0.3.0

## Step 2: Test LLM Service Import

```powershell
python -c "from core.llm_service import LLMService; print('OK')"
```

**Expected**: No errors, prints "OK"

## Step 3: Start Backend

```powershell
python main.py
```

**Expected Output**:
```
Connected to MongoDB: career_mentor
Loaded 8 sample job descriptions
Loaded 15 sample courses
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**No Errors Should Appear**:
- ❌ No "Model not found" errors
- ❌ No AttributeError
- ⚠️  Python 3.8 warnings are OK (but upgrade recommended)

## Step 4: Test API Endpoints

### Test 1: Analyze JD
```powershell
$body = @{
    job_description = "Data Analyst position requiring SQL, Python, and Tableau"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/analyze-jd -Method POST -Body $body -ContentType "application/json"
```

**Expected**: 
- Status: 200 OK
- Response contains: `{"success": true, "data": {...}}`
- Data includes: role, required_skills, etc.

### Test 2: Analyze Profile
```powershell
$body = @{
    degree = "B.Tech Computer Science"
    skills = @("Python", "Excel")
    experience_level = "beginner"
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:8000/api/analyze-profile -Method POST -Body $body -ContentType "application/json"
```

**Expected**:
- Status: 200 OK
- Response contains: `{"success": true, "data": {...}}`
- Data includes: normalized_skills, experience_level, etc.

## Step 5: Test from Frontend

1. Open http://localhost:5173
2. Go to Analysis page
3. Paste a job description
4. Click "Analyze Job Description"
5. Enter profile information
6. Click "Analyze Profile"
7. Click "Analyze Skill Gaps"

**Expected**: All steps complete without errors

## Troubleshooting

### If Still Getting 500 Errors:

1. **Check API Key**:
   ```powershell
   cd backend
   Get-Content .env | Select-String "GEMINI_API_KEY"
   ```
   Should show a valid key (starts with AIza...)

2. **Verify Package Version**:
   ```powershell
   pip list | Select-String "google-generativeai"
   ```
   Should show >= 0.3.0

3. **Check Backend Logs**:
   Look at PowerShell window for specific error messages

4. **Test LLM Directly**:
   ```powershell
   python -c "from core.llm_service import llm_service; import asyncio; result = asyncio.run(llm_service.generate('Hello')); print(result)"
   ```
   Should return generated text (if API key is valid)
