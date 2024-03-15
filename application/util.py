from googletrans import Translator

translator = Translator()

def detect_language(text):
    # get language used
    detected_lang_data = translator.detect(text)
    # print(lang)
    lang = languages.get(detected_lang_data.lang,"Language not recognized")
    conf = detected_lang_data.confidence

    return lang, conf

def translate_txt(text, dest):
    translated_text = translator.translate(text, dest=dest)
    return translated_text.text



languages = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'ar': 'arabic',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'hi': 'hindi',
    'hu': 'hungarian',
    'is': 'icelandic',
    'id': 'indonesian',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'km': 'khmer',
    'ko': 'korean',
    'la': 'latin',
    'lv': 'latvian',
    'ml': 'malayalam',
    'mr': 'marathi',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'pl': 'polish',
    'pt': 'portuguese',
    'ro': 'romanian',
    'ru': 'russian',
    'sr': 'serbian',  
    'si': 'sinhala',
    'sk': 'slovak',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'vi': 'vietnamese',
}