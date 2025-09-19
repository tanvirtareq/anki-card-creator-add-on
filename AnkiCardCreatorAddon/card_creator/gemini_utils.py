import json

from ..logger import log

import google.generativeai as genai

import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(env_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

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
    I want to create an Anki spelling-recall flashcard. For the word "{word}", generate the following:

    1. Word: The English word itself.
    2. Meaning: Up to 3 most useful meanings, each with English explanation and Bangla translation. Use line breaks for multiple meanings.
    3. Synonyms: Up to 3 most useful synonyms for the word, each with Bangla meaning. Choose synonyms relevant to the selected meanings.
    4. Usage in Sentence: Provide 1 example sentence for each meaning, including Bangla translation in parentheses.

    Format the output as a JSON object exactly like this:

    {{
    "status":"ok/no_word_found",
    "Word": "",
    "Meanings": "",
    "Synonyms": "",
    "UsageInSentence": ""
    }}

    Do not include any extra text, only the JSON. Keep the content concise and practical for active recall.
    """

    # Using Gemini Flash
    response = model.generate_content(prompt)

    json_text = clean_json_response(response.text)

    flashcard_json = json.loads(json_text)
    return flashcard_json


