from .ai_card_creator import AICardCreator
from .utils import get_or_create_basic_gemini_model

class BasicAICardCreator(AICardCreator):
    def get_model(self):
        return get_or_create_basic_gemini_model()