from .spelling_rescue_card_creator import SpellingRescueCardCreator
from .simple_audio_card_creator import SimpleAudioCardCreator

class CardCreatorFactory:
    @staticmethod
    def get_creator(card_type, word, audio_field, deck_id, parent_dialog):
        if card_type == "Spelling Rescue":
            return SpellingRescueCardCreator(word, audio_field, deck_id, parent_dialog)
        elif card_type == "Simple Audio":
            return SimpleAudioCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            raise ValueError(f"Unknown card type: {card_type}")
