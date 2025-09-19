from aqt import mw
from aqt.utils import showWarning
from ..logger import log
from .base_card_creator import BaseCardCreator
from .utils import get_or_create_model, _get_dictionary_data, get_or_create_spelling_rescue_gemini_model
from .gemini_utils import get_word_details_from_gemini

class SpellingRescueGeminiCardCreator(BaseCardCreator):
    def create_note(self):
        model = get_or_create_spelling_rescue_gemini_model()
        dict_data = get_word_details_from_gemini(self.word)
        log.debug(f"Gemini dictionary data for '{self.word}': {dict_data}")

        if not dict_data or dict_data.get('status') != 'ok':
            showWarning(f"Could not find dictionary data for '{self.word}'.", parent=self.parent_dialog)
            return

        note = mw.col.new_note(model)
        note['Word'] = self.word
        note['Audio'] = self.audio_field
        note['Meanings'] = dict_data['Meanings']
        note['Synonyms'] = dict_data['Synonyms']
        note['UsageInSentence'] = dict_data['UsageInSentence']
        mw.col.add_note(note, self.deck_id)
        log.debug(f"Spelling Rescue note for '{self.word}' added to deck ID {self.deck_id}")
