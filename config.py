import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini model
GEMINI_MODEL_ID = "gemini-3.8-flash"

# Model parameters
PARAMETERS = {
    "temperature": 0.7,
    "max_output_tokens": 256,
}