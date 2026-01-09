"""Configuration settings"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory explicitly
# __file__ is core/config.py, so parent.parent is backend/
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / ".env"

# Try multiple paths
env_loaded = False
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    env_loaded = True
    print(f"Loaded .env from: {env_path}")
else:
    # Try current directory
    current_env = Path(".env")
    if current_env.exists():
        load_dotenv(dotenv_path=current_env, override=True)
        env_loaded = True
        print(f"Loaded .env from: {current_env.absolute()}")
    else:
        # Try parent directory
        parent_env = Path("..") / ".env"
        if parent_env.exists():
            load_dotenv(dotenv_path=parent_env, override=True)
            env_loaded = True
            print(f"Loaded .env from: {parent_env.absolute()}")

# Also try loading from current directory as fallback
if not env_loaded:
    load_dotenv(override=True)

def _load_env_manually(env_file: Path) -> dict:
    """Manually parse .env file as fallback"""
    env_vars = {}
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig strips BOM
                content = f.read()
                for line_num, line in enumerate(content.splitlines(), 1):
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip().strip('\ufeff')  # Remove BOM if present
                        value = value.strip().strip('"').strip("'")
                        env_vars[key] = value
                        if key == "GEMINI_API_KEY":
                            print(f"  [OK] Found GEMINI_API_KEY on line {line_num}, value length: {len(value)}")
        except Exception as e:
            print(f"Error manually reading .env: {e}")
            import traceback
            print(traceback.format_exc())
    return env_vars

class Settings:
    def __init__(self):
        # Get API key from environment
        raw_key = os.getenv("GEMINI_API_KEY", "")
        # Remove quotes if present
        if raw_key:
            raw_key = raw_key.strip().strip('"').strip("'")
        
        # If not found, try manual loading
        if not raw_key:
            print("Attempting manual .env loading...")
            # Try the backend .env file first
            if env_path.exists():
                print(f"  Trying: {env_path}")
                manual_env = _load_env_manually(env_path)
                raw_key = manual_env.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
                if raw_key:
                    print(f"  [OK] Loaded API key manually from .env file (length: {len(raw_key)})")
                    os.environ["GEMINI_API_KEY"] = raw_key
            # Also try current directory
            if not raw_key:
                current_env = Path(".env")
                if current_env.exists():
                    print(f"  Trying: {current_env.absolute()}")
                    manual_env = _load_env_manually(current_env)
                    raw_key = manual_env.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
                    if raw_key:
                        print(f"  [OK] Loaded API key manually from current .env file (length: {len(raw_key)})")
                        os.environ["GEMINI_API_KEY"] = raw_key
        
        self.GEMINI_API_KEY = raw_key
        
        # Verify API key was loaded
        if not self.GEMINI_API_KEY:
            print(f"WARNING: GEMINI_API_KEY not found")
            print(f"  Checked paths: {env_path}, {Path('.env').absolute()}")
            print(f"  Current working directory: {os.getcwd()}")
        else:
            print(f"SUCCESS: GEMINI_API_KEY loaded (length: {len(self.GEMINI_API_KEY)})")
    
    # These are set in __init__ but we define them here for type hints
    GEMINI_API_KEY: str = ""
    
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "career_mentor")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Model settings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    # Modern Gemini 1.5 models (requires google-generativeai >= 0.3.0)
    # Options: 'gemini-1.5-flash' (faster, cheaper) or 'gemini-1.5-pro' (more capable)
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-1.5-flash")
    
    # RAG settings
    TOP_K_RESULTS: int = 5
    
    # JWT settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production-use-random-string")
    
    # Email settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", os.getenv("SMTP_USER", ""))

# Create settings instance (will print loading status)
settings = Settings()
