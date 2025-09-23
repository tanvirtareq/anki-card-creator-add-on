from .gemini_card_creator import GeminiCardCreator
from .utils import get_or_create_basic_gemini_model

class BasicGeminiCardCreator(GeminiCardCreator):
    def get_model(self):
        return get_or_create_basic_gemini_model()