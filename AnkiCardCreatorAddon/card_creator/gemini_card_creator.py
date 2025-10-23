from .base_card_creator import BaseCardCreator
from .gemini_utils import get_word_details_from_gemini
from aqt import mw
from aqt.utils import showWarning
from ..logger import log


class GeminiCardCreator(BaseCardCreator):
    def create_note(self):
        model = self.get_model()
        dict_data = get_word_details_from_gemini(self.word)
        log.debug(f"Gemini dictionary data for '{self.word}': {dict_data}")

        if not dict_data or dict_data.get('status') != 'ok':
            showWarning(f"Could not find dictionary data for '{self.word}'.", parent=self.parent_dialog)
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