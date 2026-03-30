from .ai_card_creator import AICardCreator
from .utils import get_or_create_word_rescue_gemini_model

class WordRescueAICardCreator(AICardCreator):
    def get_model(self):
        return get_or_create_word_rescue_gemini_model()