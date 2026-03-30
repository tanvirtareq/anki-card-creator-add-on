from ..logger import log
import ast
import re

AI_RESPONSE_JSON_FORMAT = """
{
'status': 'ok/no_word_found',
'Word': '',
'Meanings': [{'bangla': '', 'english': ''}],
'Synonyms': [{'bangla': '', 'english': ''}],
'UsageInSentence': [{'bangla': '', 'english': ''}]
}
"""

def get_ai_prompt(word):
    return f"""
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

    {AI_RESPONSE_JSON_FORMAT}

    Do not add extra fields.
    Do not include explanations, notes, or formatting outside the JSON.
    Keep content concise and practical for active recall.
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

def format_for_anki(flashcard_json):
    """
    Converts JSON object into Anki-ready string format:
    Each field will be "English (Bangla)" per line.
    """
    formatted = {}

    formatted['status'] = flashcard_json.get('status', 'no_word_found')
    formatted['Word'] = flashcard_json.get('Word', '')

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

def parse_and_format_response(response_text):
    """
    Cleans, parses, and formats the AI response for Anki.
    """
    json_text = clean_json_response(response_text)
    # Using literal_eval for single quotes sometimes used by AI, but JSON usually uses double.
    # However, existing code used ast.literal_eval.
    try:
        flashcard_json = ast.literal_eval(json_text)
    except (ValueError, SyntaxError) as e:
        log.error(f"Error parsing JSON with literal_eval: {e}. Trying simple replacement.")
        # Fallback for more standard JSON (double quotes)
        import json
        flashcard_json = json.loads(json_text)
    
    return format_for_anki(flashcard_json)
