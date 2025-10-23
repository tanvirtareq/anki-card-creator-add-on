from .non_ai_card_creator import NonAICardCreator
from .utils import get_or_create_word_rescue_model

class WordRescueCardCreator(NonAICardCreator):
    def get_model(self):
        return get_or_create_word_rescue_model()