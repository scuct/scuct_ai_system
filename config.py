import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    # LINE Bot settings
    LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")
    
    # LLM settings
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    
    # Google Sheets settings
    GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")

    # LIFF / public URL settings
    LIFF_ID = os.environ.get("LIFF_ID", "")
    PUBLIC_BASE_URL = os.environ.get("PUBLIC_BASE_URL", "")
    
    # Business logic settings
    BUYER_TAX_ID = os.environ.get("BUYER_TAX_ID", "29902605")

config = Config()
