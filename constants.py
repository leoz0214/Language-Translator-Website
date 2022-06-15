import string

ISO_639_1_CODES = { 
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa": "ny",
    "Chinese (simplified)": "zh-cn",
    "Chinese (traditional)": "zh-tw",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian Creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "he",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish (Kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (Burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Odia": "or",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots Gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uyghur": "ug",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}
LANGUAGES = list(ISO_639_1_CODES.keys())

LEGAL_USERNAME_CHARACTERS = string.digits + string.ascii_letters + "_"
LEGAL_PASSWORD_CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 32

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 256

USERNAME_GUIDANCE = f"""Your username must be {MIN_USERNAME_LENGTH}-{MAX_USERNAME_LENGTH} characters long (inclusive).
It is not case-sensitive, meaning USERNAME is the same as username.
It must not already be in use.
Legal username characters: numbers 0-9, letters Aa-Zz, and underscore _"""

PASSWORD_GUIDANCE = f"""Your password must be {MIN_PASSWORD_LENGTH}-{MAX_PASSWORD_LENGTH} characters long (inclusive).
It should contain a mixture of numbers, capital letters, small letters, and symbols.
It is case-sensitive, meaning PASSWORD is not the same as password.
Legal password characters: numbers 0-9, letters Aa-Zz, space, and symbols !"#$%&'()*+,-./:;<=>?@[\]^_`{{|}}~"""

LOGIN_GUIDANCE = """Your username is not case-sensitive, meaning USERNAME is the same as username.
Your password is case-sensitive, meaning PASSWORD is not the same as password."""

PASSWORD_FILE = "password.dat"
HASH_DEPTH_FILE = "hash_depth.dat"
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "languages": LANGUAGES,
    "default_langs": {
        "from": "Detect Language",
        "to": "English"
    },
    "character_limit": 10000,
}

MIN_LANGUAGES_TO_SELECT = 2

SELECT_LANGUAGES_GUIDANCE = f"""These are the languages which will be available in the translator.
Only selecting the languages you need helps reduce clutter.

All languages are selected by default.
Select at least {MIN_LANGUAGES_TO_SELECT} languages."""

DEFAULT_LANGUAGES_GUIDANCE = f"""These are the languages which will be set to the language you are translating from and to by default.
The languages you choose here must be selected above.

Select the languages you use most commonly to leverage this feature.
The default options are: from - Detect Language, to - English."""

CHARACTER_LIMIT_GUIDANCE = """This is the maximum number of characters the source text can be.

The range for this option is 100 (minimum) to 10000 (maximum).
The default maximum character count for source text is 10000."""

MIN_CHARACTER_LIMIT = 100
MAX_CHARACTER_LIMIT = 10000

EXPECTED_SETTINGS_FORM_KEYS = [
    "Detect Language",
    "default-from-language-selection",
    "default-to-language-selection",
    "character-limit" 
] + LANGUAGES

MAX_NUMBER_OF_SAVED_TRANSLATIONS = 256
MAX_TOTAL_SAVED_TRANSLATIONS_SIZE = 1024*100 # 100 KB

MAX_SAVED_TRANSLATION_NAME_LENGTH = 128