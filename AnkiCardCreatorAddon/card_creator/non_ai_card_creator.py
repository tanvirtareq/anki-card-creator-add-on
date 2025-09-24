from .base_card_creator import BaseCardCreator
from .utils import _get_dictionary_data
from aqt import mw
from aqt.utils import showWarning
from ..logger import log

class NonAICardCreator(BaseCardCreator):
    def create_note(self):
        model = self.get_model()
        dict_data = _get_dictionary_data(self.word)
        if not dict_data:
            showWarning(f"Could not find dictionary data for '{self.word}'.", parent=self.parent_dialog)
            return None

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
        return note

    def get_model(self):
        raise NotImplementedError("Subclasses must implement get_model method.")
