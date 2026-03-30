from .word_rescue_card_creator import WordRescueCardCreator
from .word_rescue_ai_card_creator import WordRescueAICardCreator
from ..logger import log
from .spelling_rescue_card_creator import SpellingRescueCardCreator
from .simple_audio_card_creator import SimpleAudioCardCreator
from .spelling_rescue_ai_card_creator import SpellingRescueAICardCreator
from .basic_card_creator import BasicCardCreator
from .basic_ai_card_creator import BasicAICardCreator

class CardCreatorFactory:
    @staticmethod
    def get_creator(card_type, word, audio_field, deck_id, parent_dialog, ai_provider):
        log.debug(f"CardCreatorFactory: Getting creator for type '{card_type}' with Provider='{ai_provider}'")
        if card_type == "Spelling Rescue":
            return CardCreatorFactory.get_spelling_rescue_creator(word, audio_field, deck_id, parent_dialog, ai_provider)
        elif card_type == "Basic":
            return CardCreatorFactory.get_basic_card_creator(word, audio_field, deck_id, parent_dialog, ai_provider)
        elif card_type == "Word Rescue":
            return CardCreatorFactory.get_word_rescue_creator(word, audio_field, deck_id, parent_dialog, ai_provider)
        elif card_type == "Simple Audio":
            return SimpleAudioCardCreator(word, audio_field, deck_id, parent_dialog)
        else:
            raise ValueError(f"Unknown card type: {card_type}")

    @staticmethod
    def get_spelling_rescue_creator(word, audio_field, deck_id, parent_dialog, ai_provider):
        log.debug(f"CardCreatorFactory: Getting Spelling Rescue creator with Provider='{ai_provider}'")
        if ai_provider in ["Gemini", "Ollama"]:
            return SpellingRescueAICardCreator(word, audio_field, deck_id, parent_dialog, ai_provider)
        else:
            return SpellingRescueCardCreator(word, audio_field, deck_id, parent_dialog)
        
    @staticmethod
    def get_basic_card_creator(word, audio_field, deck_id, parent_dialog, ai_provider):
        log.debug(f"CardCreatorFactory: Getting Basic creator with Provider='{ai_provider}'")
        if ai_provider in ["Gemini", "Ollama"]:
            return BasicAICardCreator(word, audio_field, deck_id, parent_dialog, ai_provider)
        else:
            return BasicCardCreator(word, audio_field, deck_id, parent_dialog)
    
    @staticmethod
    def get_word_rescue_creator(word, audio_field, deck_id, parent_dialog, ai_provider):
        log.debug(f"CardCreatorFactory: Getting Word Rescue creator with Provider='{ai_provider}'")
        if ai_provider in ["Gemini", "Ollama"]:
            return WordRescueAICardCreator(word, audio_field, deck_id, parent_dialog, ai_provider)
        else:
            return WordRescueCardCreator(word, audio_field, deck_id, parent_dialog)