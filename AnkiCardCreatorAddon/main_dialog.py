import os
import requests
from gtts import gTTS
from deep_translator import GoogleTranslator
import eng_to_ipa as ipa

# Import the logger instance from the main __init__.py
from . import log

from aqt import mw
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
)
from aqt.utils import showWarning, tooltip

# --- Dictionary and Translation Logic ---

def _get_dictionary_data(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response.raise_for_status()
        data = response.json()[0]

        meaning = data['meanings'][0]['definitions'][0]['definition']
        synonyms = ", ".join(data['meanings'][0]['synonyms'][:3])
        sentence = next((d['example'] for m in data['meanings'] for d in m['definitions'] if 'example' in d), "")

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
        log.error(f"Could not fetch dictionary data for '{word}'", exc_info=True)
        return None

# --- Anki Model Management ---

def get_or_create_model(model_name, fields, qfmt, afmt):
    model = mw.col.models.by_name(model_name)
    if model is None:
        log.debug(f"Model '{model_name}' not found, creating it.")
        model = mw.col.models.new(model_name)
        for field in fields:
            mw.col.models.add_field(model, mw.col.models.new_field(field))
        
        template = mw.col.models.new_template("Card 1")
        template['qfmt'] = qfmt
        template['afmt'] = afmt
        mw.col.models.add_template(model, template)
        mw.col.models.add(model)
    return model

# --- Card Creator Classes (Factory Pattern) ---

class BaseCardCreator:
    def __init__(self, word, audio_field, deck_id, parent_dialog):
        self.word = word
        self.audio_field = audio_field
        self.deck_id = deck_id
        self.parent_dialog = parent_dialog

    def create_note(self):
        raise NotImplementedError

class SimpleAudioCardCreator(BaseCardCreator):
    def create_note(self):
        model = get_or_create_model(
            model_name="Simple Audio Model",
            fields=['Word', 'Phonetics', 'Audio'],
            qfmt='{{Audio}}',
            afmt='{{FrontSide}}<hr id="answer">{{Word}}<br>{{Phonetics}}'
        )
        note = mw.col.new_note(model)
        note['Word'] = self.word
        note['Phonetics'] = ipa.convert(self.word)
        note['Audio'] = self.audio_field
        mw.col.add_note(note, self.deck_id)
        log.debug(f"Simple Audio note for '{self.word}' added to deck ID {self.deck_id}")

class SpellingRescueCardCreator(BaseCardCreator):
    def create_note(self):
        model = get_or_create_model(
            model_name="Spelling Rescue Model",
            fields=['Word', 'Audio', 'Meaning (EN)', 'Meaning (BN)', 'Synonyms (EN)', 'Synonyms (BN)', 'Sentence (EN)', 'Sentence (BN)'],
            qfmt='{{Audio}}<br>{{type:Word}}',
            afmt='{{FrontSide}}<hr id="answer">'
                 '<div id="word">{{Word}}</div><br>'
                 '<b>Meaning:</b> {{Meaning (EN)}}<br><em>{{Meaning (BN)}}</em><br><br>'
                 '<b>Synonyms:</b> {{Synonyms (EN)}}<br><em>{{Synonyms (BN)}}</em><br><br>'
                 '<b>Example:</b> {{Sentence (EN)}}<br><em>{{Sentence (BN)}}</em>'
        )
        dict_data = _get_dictionary_data(self.word)
        if not dict_data:
            showWarning(f"Could not find dictionary data for '{self.word}'.", parent=self.parent_dialog)
            return

        note = mw.col.new_note(model)
        note['Word'] = self.word
        note['Audio'] = self.audio_field
        note['Meaning (EN)'] = dict_data['meaning_en']
        note['Meaning (BN)'] = dict_data['meaning_bn']
        note['Synonyms (EN)'] = dict_data['synonyms_en']
        note['Synonyms (BN)'] = dict_data['synonyms_bn']
        note['Sentence (EN)'] = dict_data['sentence_en']
        note['Sentence (BN)'] = dict_data['sentence_bn']
        mw.col.add_note(note, self.deck_id)
        log.debug(f"Spelling Rescue note for '{self.word}' added to deck ID {self.deck_id}")

class CardCreatorFactory:
    @staticmethod
    def get_creator(card_type, word, audio_field, deck_id, parent_dialog):
        if card_type == "Spelling Rescue":
            return SpellingRescueCardCreator(word, audio_field, deck_id, parent_dialog)
        elif card_type == "Simple Audio":
            return SimpleAudioCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            raise ValueError(f"Unknown card type: {card_type}")

# --- Main Dialog Class ---

class CardCreatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Anki Card Creator")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Word Input
        self.word_label = QLabel("Word or Phrase:")
        self.word_input = QLineEdit()
        layout.addWidget(self.word_label)
        layout.addWidget(self.word_input)

        # Card Type Selector
        self.type_label = QLabel("Select Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Spelling Rescue", "Simple Audio"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)

        # Create Button
        self.create_button = QPushButton("Create Card")
        self.create_button.clicked.connect(self.on_create_card)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def on_create_card(self):
        word = self.word_input.text().strip()
        card_type = self.type_combo.currentText()
        deck_id = mw.col.decks.current()['id']

        if not word:
            showWarning("Input word cannot be empty.")
            return

        self.create_button.setEnabled(False)
        self.create_button.setText("Creating...")
        mw.progress.start(label=f"Creating card for '{word}'...")

        try:
            log.debug(f"Creating card for '{word}' of type '{card_type}'")
            # 1. Generate and add audio
            tts = gTTS(text=word, lang='en')
            audio_filename = f"ankicardcreator_{word.replace(' ', '_')}.mp3"
            # Use a temporary path first, then add to media collection
            temp_audio_path = os.path.join(mw.pm.base, audio_filename)
            tts.save(temp_audio_path)
            # Add file to media collection and get the final filename
            final_audio_filename = mw.col.media.add_file(temp_audio_path)
            audio_field = f"[sound:{final_audio_filename}]"
            log.debug(f"Audio saved and added to collection as {final_audio_filename}")

            # Use the factory to create the appropriate card
            creator = CardCreatorFactory.get_creator(card_type, word, audio_field, deck_id, self)
            creator.create_note()
            
            tooltip(f"Card for '{word}' created!", parent=self)
            self.word_input.clear()

        except Exception as e:
            log.error("An error occurred during card creation.", exc_info=True)
            showWarning(f"An error occurred: {e}")
        finally:
            mw.progress.finish()
            self.create_button.setEnabled(True)
            self.create_button.setText("Create Card")

def show_main_dialog():
    dialog = CardCreatorDialog(mw)
    log.debug("Showing main dialog.")
    dialog.show()
