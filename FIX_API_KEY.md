# Fix: 500 Error - Invalid API Key

## Problem
You're getting a 500 Internal Server Error with message:
```
API key not valid. Please pass a valid API key.
```

## Solution

### Step 1: Get a Valid Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key (starts with `AIza...`)

### Step 2: Update .env File

1. Open `backend/.env` file
2. Update the line:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Replace `your_actual_api_key_here` with your actual API key
4. Save the file

### Step 3: Restart Backend Server

1. Stop the backend server (Ctrl+C in PowerShell window)
2. Restart it:
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   python main.py
   ```

### Step 4: Test Again

Try analyzing a job description again. The error should be resolved.

## Verification

To verify your API key is set correctly:

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -c "from core.config import settings; print('API Key set:', 'Yes' if settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 20 else 'No')"
```

Should output: `API Key set: Yes`

## Common Issues

1. **API Key Not Saved**: Make sure you saved the `.env` file after editing
2. **Wrong File**: Ensure you're editing `backend/.env`, not `.env.example`
3. **Extra Spaces**: Make sure there are no spaces around the `=` sign
4. **Quotes**: Don't add quotes around the API key value
5. **Invalid Key**: Make sure you copied the entire API key from Google

## Alternative: Check Current API Key

```powershell
cd backend
Get-Content .env | Select-String "GEMINI_API_KEY"
```

This will show your current API key configuration.
