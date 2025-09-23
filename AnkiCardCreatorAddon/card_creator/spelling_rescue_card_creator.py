from aqt import mw
from aqt.utils import showWarning

from .non_ai_card_creator import NonAICardCreator
from ..logger import log
from .utils import get_spelling_rescue_model

class SpellingRescueCardCreator(NonAICardCreator):
    def get_model(self):
        return get_spelling_rescue_model()