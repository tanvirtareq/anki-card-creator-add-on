from .base_card_creator import BaseCardCreator
from .gemini_utils import get_word_details_from_gemini
from .ollama_utils import get_word_details_from_ollama
from aqt import mw
from aqt.utils import showWarning
from ..logger import log


class AICardCreator(BaseCardCreator):
    def __init__(self, word, audio_field, deck_id, parent_dialog, provider):
        super().__init__(word, audio_field, deck_id, parent_dialog)
        self.provider = provider
        log.debug(f"AICardCreator initialized with provider: {self.provider}")

    def create_note(self):
        model = self.get_model()
        
        if self.provider == "Gemini":
            dict_data = get_word_details_from_gemini(self.word)
        elif self.provider == "Ollama":
            dict_data = get_word_details_from_ollama(self.word)
        else:
            log.error(f"Unknown AI provider: {self.provider}")
            return None

        log.debug(f"{self.provider} dictionary data for '{self.word}': {dict_data}")

        if not dict_data or dict_data.get('status') == 'error':
            showWarning(f"Could not find dictionary data for '{self.word}' using {self.provider}.", parent=self.parent_dialog)
            return None
        
        if dict_data.get('status') == 'no_word_found':
            showWarning(f"No word found for '{self.word}' using {self.provider}.", parent=self.parent_dialog)
            return None

        note = mw.col.new_note(model)
        note['Word'] = self.word
        note['Audio'] = self.audio_field
        note['Meanings'] = dict_data['Meanings']
        note['Synonyms'] = dict_data['Synonyms']
        note['UsageInSentence'] = dict_data['UsageInSentence']
        mw.col.add_note(note, self.deck_id)
        return note

    def get_model(self):
        raise NotImplementedError("Subclasses must implement get_model method.")
