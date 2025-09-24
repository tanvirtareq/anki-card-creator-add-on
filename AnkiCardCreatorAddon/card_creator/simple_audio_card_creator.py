from .base_card_creator import BaseCardCreator
from .utils import get_or_create_model
from aqt import mw
from ..logger import log
import eng_to_ipa as ipa

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
        return note
