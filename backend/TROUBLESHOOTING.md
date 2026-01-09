# Troubleshooting Guide

## Common Errors and Solutions

### 500 Internal Server Error on /api/analyze-jd

#### Possible Causes:

1. **Invalid or Missing Gemini API Key**
   - Check `backend/.env` file exists
   - Verify `GEMINI_API_KEY` is set correctly
   - Get API key from: https://makersuite.google.com/app/apikey

2. **Model Not Available in Old API**
   - Old API (0.1.0rc1) doesn't support 'gemini-pro'
   - Code automatically maps to 'models/text-bison-001' for old API
   - If still failing, check API key is valid

3. **API Rate Limits or Quota Exceeded**
   - Check your Gemini API quota
   - Wait a few minutes and try again

#### Debug Steps:

1. Check backend logs in PowerShell window
2. Verify API key in `.env` file
3. Test API key manually:
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   python -c "from core.config import settings; print('API Key set:', 'Yes' if settings.GEMINI_API_KEY else 'No')"
   ```

### MongoDB Connection Errors

- Verify MongoDB Atlas connection string in `.env`
- Check network connectivity
- Ensure IP whitelist includes your IP in MongoDB Atlas

### Frontend Can't Connect to Backend

- Verify backend is running on port 8000
- Check CORS settings in `backend/main.py`
- Verify proxy in `frontend/vite.config.js`
