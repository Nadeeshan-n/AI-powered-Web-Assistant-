import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

# Model configuration
DEFAULT_MODEL = "gemini"
SUPPORTED_MODELS = ["gemini", "llama3"]
