# Import Performance Fix

## Issue
During uvicorn reload, imports were hanging because:
1. `rag_service` was loading `SentenceTransformer` at import time (slow)
2. This caused KeyboardInterrupt during multiprocessing spawn

## Fix Applied

### 1. Lazy RAG Service Initialization
**File**: `backend/core/rag_service.py`

- Changed `embedding_model` to lazy property
- Model only loads when first used, not at import time
- Speeds up imports significantly

### 2. Delayed LLM Service Message
**File**: `backend/core/llm_service_http.py`

- Service still created at import, but message printing is cleaner
- Avoids unnecessary output during reload

### 3. Uvicorn Reload Delay
**File**: `backend/main.py`

- Added `reload_delay=1.0` to prevent rapid reloads
- Helps with Windows multiprocessing issues

## Result
- ✅ Faster imports
- ✅ No hanging during reload
- ✅ Embedding model loads only when needed
- ✅ Better performance overall
