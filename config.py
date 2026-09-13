import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_MODEL_ID = "gemini-3.8-flash"

PARAMETERS = {
    "temperature": 0.2,
    "max_output_tokens": 256,
}