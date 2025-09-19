
import webview
import os
import random
import string
from gtts import gTTS
import genanki
import eng_to_ipa as ipa

# Define the directory for media files
media_dir = os.path.join(os.path.dirname(__file__), "media")
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# --- Anki Generation ---

# Model for the Anki card
ANKI_MODEL = genanki.Model(
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

# Deck for the Anki cards
ANKI_DECK = genanki.Deck(
    20594001,
    'Generated Cards'
)

def generate_random_filename(length=10):
    """Generate a random string of letters and digits."""
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))

class Api:
    """
    API class exposed to the JavaScript frontend.
    """
    def create_card(self, word):
        if not word or not word.strip():
            return {"status": "error", "message": "Input word cannot be empty."}

        try:
            # --- Audio Generation ---
            tts = gTTS(text=word, lang='en')
            audio_filename_base = generate_random_filename()
            audio_filename = f"{audio_filename_base}.mp3"
            audio_path = os.path.join(media_dir, audio_filename)
            tts.save(audio_path)

            # --- Phonetics ---
            phonetics = ipa.convert(word)

            # --- Anki Note Creation ---
            note = genanki.Note(
                model=ANKI_MODEL,
                fields=[word, phonetics, f'[sound:{audio_filename}]']
            )
            ANKI_DECK.add_note(note)

            # --- Package Creation ---
            package = genanki.Package(ANKI_DECK)
            package.media_files = [audio_path]
            package.write_to_file('output.apkg')

            return {"status": "success", "message": f"Successfully created card for '{word}'. Find it in output.apkg."}
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {e}"}

if __name__ == '__main__':
    api = Api()
    # Create the webview window
    webview.create_window(
        'Anki Card Creator',
        'static/index.html',
        js_api=api,
        width=550,
        height=400
    )
    webview.start()
