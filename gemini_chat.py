import google.generativeai as genai
import os
import time
from google.api_core.exceptions import ResourceExhausted

os.environ["GEMINI_API_KEY"] = "AIzaSyBTtLkmnv7zQz4SxeAJD5H06xdSY9dC1JI"

def get_gemini_response(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "⚠️ Gemini API key not found. Please set GEMINI_API_KEY."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    chat = model.start_chat()

    # Retry logic for temporary quota errors
    for attempt in range(3):
        try:
            reply = chat.send_message(prompt)
            return reply.text
        except ResourceExhausted:
            wait_time = (attempt + 1) * 10
            print(f"⚠️ Gemini quota exhausted, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            return f"⚠️ Gemini error: {e}"

    return "🚫 Gemini API quota exhausted. Please try again later."
