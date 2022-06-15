from constants import *
from filehandling import *
from savedtranslations import *


def valid_sign_up_credentials(username: str, password: str, confirm_password: str):
    return all((
        valid_sign_up_username(username),
        valid_sign_up_password(password),
        valid_sign_up_confirm_password(password, confirm_password)
    ))


def valid_login_credentials(username: str, password: str):
    return not has_illegal_characters(username, LEGAL_USERNAME_CHARACTERS)\
    and username_is_taken(username)\
    and password_matches(username, password)


def valid_change_password_credentials(current: str, new: str, confirm_new: str):
    return all((
        valid_sign_up_password(new),
        valid_sign_up_confirm_password(new, confirm_new),
        new != current
    ))


def valid_settings(form_keys: tuple, selected_languages: list, default_languages: dict, character_limit: int):
    return all((
        valid_form_keys(form_keys),
        valid_selected_languages(selected_languages),
        valid_default_languages(selected_languages, default_languages),
        valid_character_limit(character_limit)
    ))


def valid_saved_translation(username: str, name: str, from_lang: str, source_text: str, to_lang: str, translation: str, name_exists: str):
    return all((
        valid_saved_translation_name(name),
        valid_saved_translation_language(from_lang),
        valid_source_text(source_text),
        valid_saved_translation_language(to_lang),
        valid_translation(translation),
        valid_name_exists(username, name, name_exists)
    ))


def valid_sign_up_username(username: str):
    return all((
        isinstance(username, str),
        MIN_USERNAME_LENGTH <= len(username) <= MAX_USERNAME_LENGTH,
        not has_illegal_characters(username, LEGAL_USERNAME_CHARACTERS),
    ))


def valid_sign_up_password(password: str):
    return all((
        isinstance(password, str),
        MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH,
        not has_illegal_characters(password, LEGAL_PASSWORD_CHARACTERS)
    ))


def valid_sign_up_confirm_password(password, confirm_password: str):
    return isinstance(confirm_password, str) and confirm_password == password


def has_illegal_characters(string: str, legal_characters: str):
    return any(character not in legal_characters for character in string)


def username_is_taken(username: str):
    return folder_exists(f"accounts/{username}")


def password_matches(username: str, password: str):
    hash_depth = int(read_file(f"accounts/{username}/{HASH_DEPTH_FILE}", binary=True))
    registered_password = read_file(f"accounts/{username}/{PASSWORD_FILE}", binary=True, is_compressed=True).decode()
    return hash_string(password, hash_depth) == registered_password


def valid_form_keys(form_keys: tuple):
    return all(key in EXPECTED_SETTINGS_FORM_KEYS for key in form_keys)


def valid_selected_languages(languages: list):
    return all((
        len(languages) >= MIN_LANGUAGES_TO_SELECT,
        all(language in LANGUAGES for language in languages)
    ))


def valid_default_languages(selected_languages: list, default_languages: dict):
    return all((
        default_languages["from"] in ["Detect Language"] + selected_languages,
        default_languages["to"] in selected_languages,
        len(default_languages) == 2
    ))


def valid_character_limit(character_limit: int):
    return all((
        MIN_CHARACTER_LIMIT <= character_limit <= MAX_CHARACTER_LIMIT,
        character_limit % 100 == 0
    ))


def valid_saved_translation_name(name: str):
    return isinstance(name, str) and 1 <= len(name) <= MAX_SAVED_TRANSLATION_NAME_LENGTH


def valid_saved_translation_language(language: str):
    return isinstance(language, str) and language in LANGUAGES


def valid_source_text(source_text: str):
    return isinstance(source_text, str) and len(source_text) <= MAX_CHARACTER_LIMIT


def valid_translation(translation: str):
    return isinstance(translation, str) and translation == translation.strip()


def valid_name_exists(username: str, name: str, name_exists: bool):
    return isinstance(name_exists, bool) and name_exists == SavedTranslations(username).name_exists(name)