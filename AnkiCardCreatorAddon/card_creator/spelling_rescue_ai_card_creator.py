from .ai_card_creator import AICardCreator
from .utils import get_or_create_spelling_rescue_gemini_model

class SpellingRescueAICardCreator(AICardCreator):
    def get_model(self):
        return get_or_create_spelling_rescue_gemini_model()