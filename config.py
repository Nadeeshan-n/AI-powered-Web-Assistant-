import os
from dotenv import load_dotenv

load_dotenv()

AI_PROVIDER = os.getenv("AI_PROVIDER", "openrouter").lower()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")

HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL = os.getenv("HF_MODEL", "openai/gpt-oss-120b:fastest")

PARAMETERS = {
    "temperature": float(os.getenv("AI_TEMPERATURE", "0.2")),
    "max_output_tokens": int(os.getenv("AI_MAX_OUTPUT_TOKENS", "512")),
}