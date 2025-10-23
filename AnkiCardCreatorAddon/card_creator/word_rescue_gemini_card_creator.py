
from .utils import get_or_create_word_rescue_gemini_model
from .gemini_card_creator import GeminiCardCreator

class WordRescueGeminiCardCreator(GeminiCardCreator):
    def get_model(self):
        return get_or_create_word_rescue_gemini_model()