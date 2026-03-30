import ollama
from ..logger import log
from .ai_utils import get_ai_prompt, parse_and_format_response

def get_word_details_from_ollama(word):
    """
    Fetches word details from Ollama and formats them for Anki.
    """
    prompt = get_ai_prompt(word)
    log.debug(f"Ollama prompt for '{word}': {prompt}")

    try:
        # Using gemma3:1b as default
        response = ollama.chat(
            model='gemma3:1b',
            messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ],
        )

        raw_response = response['message']['content']
        log.debug(f"Ollama raw response for '{word}': {raw_response}")

        # Process response
        formatted_data = parse_and_format_response(raw_response)
        log.debug(f"Ollama processed response for '{word}': {formatted_data}")
        return formatted_data

    except Exception as e:
        log.error(f"Error calling Ollama for '{word}': {e}", exc_info=True)
        # If Ollama is not running or model not found, handle gracefully
        return {'status': 'error', 'Word': word}
