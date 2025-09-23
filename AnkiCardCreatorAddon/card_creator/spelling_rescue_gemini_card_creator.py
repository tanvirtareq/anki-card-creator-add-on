from .gemini_card_creator import GeminiCardCreator
from .utils import get_or_create_spelling_rescue_gemini_model

class SpellingRescueGeminiCardCreator(GeminiCardCreator):
    def get_model(self):
        return get_or_create_spelling_rescue_gemini_model()
    