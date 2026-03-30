import os
from dotenv import load_dotenv
import google.generativeai as genai
from ..logger import log
from .ai_utils import get_ai_prompt, clean_json_response, parse_and_format_response

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    log.error("GEMINI_API_KEY not found in environment.")
    model = None

def get_word_details_from_gemini(word):
    """
    Fetches word details from Gemini and formats them for Anki.
    """
    if not model:
        log.error("Gemini model not initialized.")
        return {'status': 'error', 'Word': word}

    prompt = get_ai_prompt(word)
    log.debug(f"Gemini prompt for '{word}': {prompt}")

    # Generate content
    try:
        response = model.generate_content(prompt)
        log.debug(f"Gemini raw response for '{word}': {response.text}")

        # Process response
        formatted_data = parse_and_format_response(response.text)
        log.debug(f"Gemini processed response for '{word}': {formatted_data}")
        return formatted_data

    except Exception as e:
        log.error(f"Error calling Gemini for '{word}': {e}", exc_info=True)
        return {'status': 'error', 'Word': word}
