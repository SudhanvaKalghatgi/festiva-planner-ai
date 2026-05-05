from dotenv import load_dotenv
import os
import time
from google import genai

# 🔥 Load env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

# 🔥 NEW SDK CLIENT (correct way)
client = genai.Client(api_key=API_KEY)

# 🔥 Model fallback list
MODEL_CANDIDATES = [
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

# 🔥 Rate limiting
LAST_CALL = 0
MIN_INTERVAL = 2


def _call_with_fallback(prompt: str):
    global LAST_CALL

    for model_name in MODEL_CANDIDATES:
        try:
            now = time.time()

            # 🔥 Rate limit protection
            if now - LAST_CALL < MIN_INTERVAL:
                time.sleep(MIN_INTERVAL - (now - LAST_CALL))

            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )

            LAST_CALL = time.time()

            if response and hasattr(response, "text") and response.text:
                return response.text

        except Exception as e:
            print(f"❌ Model failed: {model_name} -> {e}")
            continue

    return None


def polish_response(text: str) -> str:
    prompt = f"""
You are an assistant that improves readability of structured planning outputs.

STRICT RULES:
- Do NOT change numbers
- Do NOT add new facts
- Do NOT remove warnings
- Do NOT modify financial values
- Only improve clarity, formatting, and flow
- Keep it concise and professional

CONTENT:
{text}
"""

    try:
        result = _call_with_fallback(prompt)
        return result if result else text
    except Exception:
        return text