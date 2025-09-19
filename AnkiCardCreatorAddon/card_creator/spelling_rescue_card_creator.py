from aqt import mw
from aqt.utils import showWarning
from ..logger import log
from .base_card_creator import BaseCardCreator
from .utils import get_or_create_model, _get_dictionary_data

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
