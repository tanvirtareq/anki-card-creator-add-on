import requests
from deep_translator import GoogleTranslator
from ..logger import log
from aqt import mw

def _get_dictionary_data(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        response.raise_for_status()
        data = response.json()[0]

        meaning = data['meanings'][0]['definitions'][0]['definition']
        synonyms = ", ".join(data['meanings'][0]['synonyms'][:3])
        sentence = next((d['example'] for m in data['meanings'] for d in m['definitions'] if 'example' in d), "")

        meaning_bn = GoogleTranslator(source='auto', target='bn').translate(meaning)
        synonyms_bn = GoogleTranslator(source='auto', target='bn').translate(synonyms)
        sentence_bn = GoogleTranslator(source='auto', target='bn').translate(sentence)

        return {
            "meaning_en": meaning,
            "meaning_bn": meaning_bn,
            "synonyms_en": synonyms,
            "synonyms_bn": synonyms_bn,
            "sentence_en": sentence,
            "sentence_bn": sentence_bn,
        }
    except Exception:
        log.error(f"Could not fetch dictionary data for '{word}'", exc_info=True)
        return None

# --- Anki Model Management ---

def get_or_create_model(model_name, fields, qfmt, afmt):
    model = mw.col.models.by_name(model_name)
    if model is None:
        log.debug(f"Model '{model_name}' not found, creating it.")
        model = mw.col.models.new(model_name)
        for field in fields:
            mw.col.models.add_field(model, mw.col.models.new_field(field))
        
        template = mw.col.models.new_template("Card 1")
        template['qfmt'] = qfmt
        template['afmt'] = afmt
        mw.col.models.add_template(model, template)
        mw.col.models.add(model)
    return model
