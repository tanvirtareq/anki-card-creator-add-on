class BaseCardCreator:
    def __init__(self, word, audio_field, deck_id, parent_dialog):
        self.word = word
        self.audio_field = audio_field
        self.deck_id = deck_id
        self.parent_dialog = parent_dialog

    def create_note(self):
        raise NotImplementedError