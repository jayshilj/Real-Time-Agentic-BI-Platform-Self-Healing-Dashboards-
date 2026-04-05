import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# Validate key exists at startup
if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Add it to your .env file: GEMINI_API_KEY=your_key_here"
    )

# Agent config
POLL_INTERVAL_SECONDS = 30
MAX_HEAL_RETRIES = 3