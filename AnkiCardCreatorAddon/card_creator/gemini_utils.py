import ast

from ..logger import log

import google.generativeai as genai

import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

GEMINI_RESPONSE_JSON_FORMAT = """
{
'status': 'ok/no_word_found',
'Word': '',
'Meanings': [{'bangla': '', 'english': ''}],
'Synonyms': [{'bangla': '', 'english': ''}],
'UsageInSentence': [{'bangla': '', 'english': ''}]
}
"""

def clean_json_response(response_text):
    """
    Cleans the response text to extract valid JSON.
    """
    try:
        # Attempt to find the first and last curly braces
        start_index = response_text.index('{')
        end_index = response_text.rindex('}') + 1
        json_text = response_text[start_index:end_index]
        return json_text
    except ValueError as e:
        log.error(f"Error extracting JSON from response: {e}")
        raise

def get_word_details_from_gemini(word):

    prompt = f"""
    Generate a JSON object for an Anki flashcard for the word {word}. Follow these exact rules:

    1. Word: The English word itself.
    2. Meanings: Up to 3 of the most useful meanings. Each meaning must include:
    "english" → English explanation (short and clear).
    "bangla" → Bangla translation.
    Use line breaks if there are multiple meanings.

    3. Synonyms: Up to 3 synonyms related to the given meanings. Each synonym must include:
    "english" → synonym in English.
    "bangla" → synonym meaning in Bangla.

    4. Usage in Sentence: Provide 1 example sentence per meaning. Each must include:
    "english" → example sentence.
    "bangla" → Bangla translation of the sentence.

    5. Format: The output must always be a valid JSON object in this exact structure:

    {GEMINI_RESPONSE_JSON_FORMAT}

    Do not add extra fields.
    Do not include explanations, notes, or formatting outside the JSON.
    Keep content concise and practical for active recall.
    """

    log.debug(f"Gemini prompt for '{word}': {prompt}")

    # Using Gemini Flash
    response = model.generate_content(prompt)

    log.debug(f"Gemini raw response for '{word}': {response.text}")

    json_text = clean_json_response(response.text)
    log.debug(f"Gemini cleaned response for '{word}': {json_text}")

    flashcard_json = ast.literal_eval(json_text)

    log.debug(f"Gemini JSON response for '{word}': {flashcard_json}")

    return format_for_anki(flashcard_json)

def format_for_anki(flashcard_json):
    """
    Converts JSON object into Anki-ready string format:
    Each field will be "English (Bangla)" per line.
    """
    formatted = {}

    formatted['status'] = flashcard_json['status']
    formatted['Word'] = flashcard_json['Word']

    # Format meanings
    meanings = flashcard_json.get('Meanings', [])
    formatted_meanings = [f"{i+1}. {m['english']} ({m['bangla']})" for i, m in enumerate(meanings)]
    formatted['Meanings'] = ",<br>".join(formatted_meanings)

    # Format synonyms
    synonyms = flashcard_json.get('Synonyms', [])
    formatted_synonyms = [f"{i+1}. {s['english']} ({s['bangla']})" for i, s in enumerate(synonyms)]
    formatted['Synonyms'] = ",<br>".join(formatted_synonyms)

    # Format usage sentences
    usage = flashcard_json.get('UsageInSentence', [])
    formatted_usage = [f"{i+1}. {u['english']} ({u['bangla']})" for i, u in enumerate(usage)]
    formatted['UsageInSentence'] = ",<br>".join(formatted_usage)

    return formatted
