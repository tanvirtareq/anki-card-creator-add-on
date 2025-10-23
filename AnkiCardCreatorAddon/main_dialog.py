import os
import re
from gtts import gTTS

# Import the logger instance from the main __init__.py
from . import log
from .card_creator.card_creator_factory import CardCreatorFactory

from aqt import QCheckBox, mw
from aqt.qt import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QTextEdit,
)
from aqt.utils import showWarning, tooltip
from aqt import sound

# --- Dictionary and Translation Logic ---

class CardDataDialog(QDialog):
    def __init__(self, note, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Created Card Data")
        self.setup_ui(note)

    def setup_ui(self, note):
        layout = QVBoxLayout(self)

        for name, value in note.items():
            h_layout = QHBoxLayout()
            name_label = QLabel(f"<b>{name}:</b>")
            name_label.setFixedWidth(100) # Adjust width as needed
            h_layout.addWidget(name_label)

            if name == 'Audio' and value:
                # Extract filename from [sound:...] tag
                match = re.search(r'\[sound:(.*?)\]', value)
                if match:
                    audio_file = match.group(1)
                    value_label = QLabel(audio_file)
                    play_button = QPushButton("Play")
                    play_button.clicked.connect(lambda _, a=audio_file: self.play_audio(a))
                    h_layout.addWidget(value_label)
                    h_layout.addWidget(play_button)
                else:
                    value_label = QLabel(value)
                    h_layout.addWidget(value_label)
            else:
                value_label = QLabel(value)
                value_label.setWordWrap(True)
                h_layout.addWidget(value_label)

            layout.addLayout(h_layout)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
        self.setMinimumSize(500, 300)

    def play_audio(self, audio_file):
        sound.play(audio_file)

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
        self.type_combo.addItems(["Spelling Rescue", "Basic", "Word Rescue", "Simple Audio"])
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)


        # Create Checkbox for "Use Gemini"
        self.use_gemini_checkbox = QCheckBox("Use Gemini")
        layout.addWidget(self.use_gemini_checkbox)

        # Create Button
        self.create_button = QPushButton("Create Card")
        self.create_button.clicked.connect(self.on_create_card)
        layout.addWidget(self.create_button)

        self.setLayout(layout)

    def on_create_card(self):
        word = self.word_input.text().strip()
        card_type = self.type_combo.currentText()
        deck_id = mw.col.decks.current()['id']
        use_gemini = self.use_gemini_checkbox.isChecked()
        # Log the Gemini usage
        log.debug(f"Use Gemini: {use_gemini}")

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
            creator = CardCreatorFactory.get_creator(card_type, word, audio_field, deck_id, self, use_gemini)
            note = creator.create_note()

            if note:
                tooltip(f"Card for '{word}' created!", parent=self)
                self.word_input.clear()
                # Show the card data in a new window
                self.card_data_dialog = CardDataDialog(note, self)
                self.card_data_dialog.show()

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
