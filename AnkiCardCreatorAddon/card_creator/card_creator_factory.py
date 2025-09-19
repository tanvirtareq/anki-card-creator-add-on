from ..logger import log
from .spelling_rescue_card_creator import SpellingRescueCardCreator
from .simple_audio_card_creator import SimpleAudioCardCreator

from .spelling_rescue_gemini_card_creator import SpellingRescueGeminiCardCreator

class CardCreatorFactory:
    @staticmethod
    def get_creator(card_type, word, audio_field, deck_id, parent_dialog, use_gemini):
        log.debug(f"CardCreatorFactory: Getting creator for type '{card_type}' with Gemini={use_gemini}")
        if card_type == "Spelling Rescue" and use_gemini == False:
            return SpellingRescueCardCreator(word, audio_field, deck_id, parent_dialog)
        elif card_type == "Spelling Rescue" and use_gemini == True:
            return SpellingRescueGeminiCardCreator(word, audio_field, deck_id, parent_dialog)
        elif card_type == "Simple Audio":
            return SimpleAudioCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            raise ValueError(f"Unknown card type: {card_type}")
