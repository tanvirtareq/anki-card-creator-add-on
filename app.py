
import webview
import os
import random
import string
import requests
from gtts import gTTS
import genanki
import eng_to_ipa as ipa
from deep_translator import GoogleTranslator

# --- Setup ---
media_dir = os.path.join(os.path.dirname(__file__), "media")
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# --- Anki Models & Decks ---

# Model for the original simple audio card
SIMPLE_AUDIO_MODEL = genanki.Model(
    1607392319,
    'Simple Audio Model',
    fields=[
        {'name': 'Word'},
        {'name': 'Phonetics'},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Audio}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Word}}<br>{{Phonetics}}',
        },
    ])

# Model for the new Spelling Rescue card
SPELLING_RESCUE_MODEL = genanki.Model(
    1607392320, # New unique ID
    'Spelling Rescue Model',
    fields=[
        {'name': 'Word'}, # Field for the user to type into
        {'name': 'Audio'},
        {'name': 'Meaning (EN)'},
        {'name': 'Meaning (BN)'},
        {'name': 'Synonyms (EN)'},
        {'name': 'Synonyms (BN)'},
        {'name': 'Sentence (EN)'},
        {'name': 'Sentence (BN)'},
        {'name': 'Usage Tips'},
    ],
    templates=[
        {
            'name': 'Spelling Card',
            'qfmt': '{{Audio}}<br>{{type:Word}}',
            'afmt': '{{FrontSide}}<hr id="answer">'
                    '<div id="word">{{Word}}</div><br>'
                    '<b>Meaning:</b> {{Meaning (EN)}}<br><em>{{Meaning (BN)}}</em><br><br>'
                    '<b>Synonyms:</b> {{Synonyms (EN)}}<br><em>{{Synonyms (BN)}}</em><br><br>'
                    '<b>Example:</b> {{Sentence (EN)}}<br><em>{{Sentence (BN)}}</em><br><br>'
                    '<i>{{Usage Tips}}</i>'
        },
    ])

SIMPLE_DECK = genanki.Deck(2059400110, 'Generated Simple Cards')
SPELLING_DECK = genanki.Deck(2059400111, 'Generated Spelling Cards')

# --- Helper Functions ---

def generate_random_filename(length=10):
    """Generate a random string of letters and digits."""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

def _get_dictionary_data(word):
    """Fetches dictionary data and translates it."""
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response.raise_for_status()
        data = response.json()[0]

        # Extract data
        meaning = data['meanings'][0]['definitions'][0]['definition']
        synonyms = ", ".join(data['meanings'][0]['synonyms'][:3])
        sentence = next((d['example'] for m in data['meanings'] for d in m['definitions'] if 'example' in d), "No example found.")

        # Translate data
        meaning_bn = GoogleTranslator(source='auto', target='bn').translate(meaning)
        synonyms_bn = GoogleTranslator(source='auto', target='bn').translate(synonyms)
        sentence_bn = GoogleTranslator(source='auto', target='bn').translate(sentence)

        return {
            "meaning_en": meaning,
            "meaning_bn": meaning_bn,
            "synonyms_en": synonyms,
            "synonyms_bn": synonyms_bn,
            "sentence_en": sentence,
            "sentence_bn": sentence_bn,
        }
    except Exception:
        return None

# --- API Class for Frontend ---

class Api:
    """API class exposed to the JavaScript frontend."""

    def create_card(self, word, card_type="Simple Audio"):
        if not word or not word.strip():
            return {"status": "error", "message": "Input word cannot be empty."}

        try:
            # --- Common for all cards: Audio Generation ---
            tts = gTTS(text=word, lang='en')
            audio_filename = f"{generate_random_filename()}.mp3"
            audio_path = os.path.join(media_dir, audio_filename)
            tts.save(audio_path)
            audio_field = f'[sound:{audio_filename}]'

            # --- Card Type Dispatcher ---
            if card_type == "Spelling Rescue":
                deck = SPELLING_DECK
                dict_data = _get_dictionary_data(word)
                if not dict_data:
                    return {"status": "error", "message": f"Could not find dictionary data for '{word}'."}

                note = genanki.Note(
                    model=SPELLING_RESCUE_MODEL,
                    fields=[
                        word, 
                        audio_field,
                        dict_data['meaning_en'],
                        dict_data['meaning_bn'],
                        dict_data['synonyms_en'],
                        dict_data['synonyms_bn'],
                        dict_data['sentence_en'],
                        dict_data['sentence_bn'],
                        "Usage tips coming soon!"
                    ])
            else: # Default to Simple Audio
                deck = SIMPLE_DECK
                phonetics = ipa.convert(word)
                note = genanki.Note(
                    model=SIMPLE_AUDIO_MODEL,
                    fields=[word, phonetics, audio_field]
                )

            deck.add_note(note)
            package = genanki.Package(deck)
            package.media_files = [audio_path]
            package.write_to_file('output.apkg')

            return {"status": "success", "message": f"Successfully created '{card_type}' card for '{word}'."}

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {e}"}

if __name__ == '__main__':
    api = Api()
    webview.create_window(
        'Anki Card Creator',
        'static/index.html',
        js_api=api,
        width=550,
        height=450 # Increased height for new dropdown
    )
    webview.start()
