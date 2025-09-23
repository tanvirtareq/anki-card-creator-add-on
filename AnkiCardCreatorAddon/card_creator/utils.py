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
        
        template = mw.col.models.new_template(model_name + " Template 1")
        template['qfmt'] = qfmt
        template['afmt'] = afmt
        mw.col.models.add_template(model, template)
        mw.col.models.add(model)
    return model

NON_AI_MODEL_FIELDS = ['Word', 'Audio', 'Meaning (EN)', 'Meaning (BN)', 'Synonyms (EN)', 'Synonyms (BN)', 'Sentence (EN)', 'Sentence (BN)']


SPELLING_RECALL_BACK_TEMPLATE = """
<style>
.field-label { font-weight: bold; display: block; margin-top: 10px; }
.word-line {
  font-weight: bold;
  font-size: 40px;
}
</style>

<div class="word-line">
{{type:Word}}
</div>

<b>Meaning:</b> {{Meaning (EN)}}<br><em>{{Meaning (BN)}}</em><br><br>
<b>Synonyms:</b> {{Synonyms (EN)}}<br><em>{{Synonyms (BN)}}</em><br><br>
<b>Example:</b> {{Sentence (EN)}}<br><em>{{Sentence (BN)}}</em>

"""


def get_spelling_rescue_model():
    return get_or_create_model(
        model_name="Spelling Rescue Model",
        fields=NON_AI_MODEL_FIELDS,
        qfmt=SPELLING_RECALL_FRONT_TEMPLATE,
        afmt=SPELLING_RECALL_BACK_TEMPLATE
    )

BASIC_MODEL_BACK_TEMPLATE = """
<style>
.field-label { display: block; margin-top: 10px; }
.word-line {
  font-weight: bold;
  font-size: 50px;
}
</style>

<div class="word-line">
  {{Word}}
</div>


<b>Meaning:</b> {{Meaning (EN)}}<br><em>{{Meaning (BN)}}</em><br><br>
<b>Synonyms:</b> {{Synonyms (EN)}}<br><em>{{Synonyms (BN)}}</em><br><br>
<b>Example:</b> {{Sentence (EN)}}<br><em>{{Sentence (BN)}}</em>

"""

def get_basic_model():
    return get_or_create_model(
        model_name="Basic Model 1",
        fields=NON_AI_MODEL_FIELDS,
        qfmt=BASIC_MODEL_FRONT_TEMPLATE,
        afmt=BASIC_MODEL_BACK_TEMPLATE
    )

SPELLING_RECALL_FRONT_TEMPLATE = """
<style>
.field-label { font-weight: bold; display: block; margin-top: 10px; }

.audio-line {
  margin-bottom: 10px;
}

</style>

<div class="audio-line">
  {{Audio}}
</div>

<span class="field-label">Type the correct English word:</span>
{{type:Word}}

"""

SPELLING_RECALL_GEMINI_BACK_TEMPLATE = """
<style>
.field-label { display: block; margin-top: 10px; }
.word-line {
  font-weight: bold;
  font-size: 30px;
}
</style>

<div class="word-line">
{{type:Word}}
</div>


<span class="field-label">Correct Word:</span>
{{Word}}

<span class="field-label">Meaning:</span>
{{Meanings}}

<span class="field-label">Synonyms:</span>
{{Synonyms}}

<span class="field-label">Usage in Sentence:</span>
{{UsageInSentence}}

"""

GEMINI_MODEL_FIELDS = ['Word', 'Audio', 'Meanings', 'Synonyms', 'UsageInSentence']

def get_or_create_spelling_rescue_gemini_model():
    return get_or_create_model(
        model_name="Spelling Rescue Gemini Model",
        fields=GEMINI_MODEL_FIELDS,
        qfmt=SPELLING_RECALL_FRONT_TEMPLATE,
        afmt=SPELLING_RECALL_GEMINI_BACK_TEMPLATE
    )

BASIC_MODEL_FRONT_TEMPLATE = """
<style>
.audio-line {
  margin-bottom: 10px;
}

.word-line {
  font-weight: bold;
  font-size: 70px;
}
</style>

<div class="audio-line">
  {{Audio}}
</div>

<div class="word-line">
  {{Word}}
</div>


"""

def get_or_create_basic_gemini_model():
    return get_or_create_model(
        model_name="Basic Model Gemini 1",
        fields=GEMINI_MODEL_FIELDS,
        qfmt=BASIC_MODEL_FRONT_TEMPLATE,
        afmt=SPELLING_RECALL_GEMINI_BACK_TEMPLATE
    )