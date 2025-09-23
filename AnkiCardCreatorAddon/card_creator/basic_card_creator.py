from .non_ai_card_creator import NonAICardCreator
from .utils import get_basic_model

class BasicCardCreator(NonAICardCreator):
    def get_model(self):
        return get_basic_model()