from AnkiCardCreatorAddon.card_creator.word_rescue_card_creator import WordRescueCardCreator
from AnkiCardCreatorAddon.card_creator.word_rescue_gemini_card_creator import WordRescueGeminiCardCreator
from ..logger import log
from .spelling_rescue_card_creator import SpellingRescueCardCreator
from .simple_audio_card_creator import SimpleAudioCardCreator
from .spelling_rescue_gemini_card_creator import SpellingRescueGeminiCardCreator
from .basic_card_creator import BasicCardCreator
from .basic_gemini_card_creator import BasicGeminiCardCreator

class CardCreatorFactory:
    @staticmethod
    def get_creator(card_type, word, audio_field, deck_id, parent_dialog, use_gemini):
        log.debug(f"CardCreatorFactory: Getting creator for type '{card_type}' with Gemini={use_gemini}")
        if card_type == "Spelling Rescue":
            return CardCreatorFactory.get_spelling_rescue_creator(word, audio_field, deck_id, parent_dialog, use_gemini)
        elif card_type == "Basic":
            return CardCreatorFactory.get_basic_card_creator(word, audio_field, deck_id, parent_dialog, use_gemini)
        elif card_type == "Word Rescue":
            return CardCreatorFactory.get_word_rescue_creator(word, audio_field, deck_id, parent_dialog, use_gemini)
        elif card_type == "Simple Audio":
            return SimpleAudioCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            raise ValueError(f"Unknown card type: {card_type}")

    @staticmethod
    def get_spelling_rescue_creator(word, audio_field, deck_id, parent_dialog, use_gemini):
        log.debug(f"CardCreatorFactory: Getting Spelling Rescue creator with Gemini={use_gemini}")
        if use_gemini:
            return SpellingRescueGeminiCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            return SpellingRescueCardCreator(word, audio_field, deck_id, parent_dialog)
        
    @staticmethod
    def get_basic_card_creator(word, audio_field, deck_id, parent_dialog, use_gemini):
        log.debug(f"CardCreatorFactory: Getting Basic creator with Gemini={use_gemini}")
        if use_gemini:
            return BasicGeminiCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            return BasicCardCreator(word, audio_field, deck_id, parent_dialog)
    
    @staticmethod
    def get_word_rescue_creator(word, audio_field, deck_id, parent_dialog, use_gemini):
        log.debug("CardCreatorFactory: Getting Word Rescue creator")
        if use_gemini:
            return WordRescueGeminiCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            return WordRescueCardCreator(word, audio_field, deck_id, parent_dialog)