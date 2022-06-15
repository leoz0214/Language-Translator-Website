# Translator Website - HTML5, CSS3, JavaScript, Python 3.10.1
# Approx 1000 lines of 'clean' code as of night 5th June 2022
# Week 2 - critical mistake - not validating input being sent to the server. Code at front end can be modified... oops. Fixing this...
# From mainly front end validation (better User Experience) to both front end and back end validation.
# Over 2000 lines of code as of night 12th June 2022
# Week 3 - help and about pages added.
# Final line count (ALL CODE FILES ALL LINES - including comments, blank lines, and ridiculously long constants): 3005.
# Final line count by technology: Python - 934 (31.08%), HTML - 914 (30.42%), CSS - 281 (9.35%), JavaScript - 876 (29.15%) 
from flask import Flask, session, request, render_template, redirect
from googletrans import Translator # pip install googletrans
from secrets import choice
from contextlib import suppress

from constants import *
from filehandling import *
from validation import *
from savedtranslations import SavedTranslations

APP = Flask(__name__)


@APP.route("/")
def index_route():
    return render_template(
        "index.html",
        username = session.get("username"),
        just_signed_up = check_for_session_event("just_signed_up"),
        just_logged_in = check_for_session_event("just_logged_in"),
        just_logged_out = check_for_session_event("just_logged_out")
    )


@APP.route("/translator", methods=("POST", "GET"))
def translator_route():
    if request.method == "POST":
        data = request.get_json()
        from_lang = ISO_639_1_CODES.get(data["from_lang"], "auto")
        source_text = data["source_text"]
        to_lang = ISO_639_1_CODES[data["to_lang"]]
        return translate(from_lang, source_text, to_lang)

    elif "username" in session:
        settings = get_settings(session["username"])

        return render_template(
            "translator.html",
            username = session["username"],
            from_langs = ["Detect Language"] + settings["languages"],
            starting_from_lang = settings["default_langs"]["from"],
            to_langs = settings["languages"],
            starting_to_lang = settings["default_langs"]["to"],
            character_limit = settings["character_limit"]
        )

    return render_template(
        "translator.html", 
        from_langs = ["Detect Language"] + LANGUAGES,
        to_langs = LANGUAGES,
        character_limit = 10000
    )


@APP.route("/sign-up", methods=("POST", "GET"))
def sign_up_route():
    if "username" in session:
        return redirect("/")
    elif request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            confirm_password = request.form["confirm-password"]
            new_folder = f"accounts/{username}"

            if valid_sign_up_credentials(username, password, confirm_password):
                if not username_is_taken(username):
                    create_folder(new_folder)
                    update_password(username, password)
                    update_settings(username, DEFAULT_SETTINGS)
                    session["just_signed_up"] = True
                    session["username"] = username
                    return redirect("/")
                
                return render_template(
                    "signup.html",
                    username_guidance = USERNAME_GUIDANCE,
                    password_guidance = PASSWORD_GUIDANCE,
                    username_now_taken = True,
                )
            
            return render_template(
                "signup.html",
                username_guidance = USERNAME_GUIDANCE,
                password_guidance = PASSWORD_GUIDANCE,
                invalid_credentials = True
            )

        except Exception:
            return render_template(
                "signup.html",
                username_guidance = USERNAME_GUIDANCE,
                password_guidance = PASSWORD_GUIDANCE,
                error = True
            )

    return render_template(
        "signup.html",
        username_guidance = USERNAME_GUIDANCE,
        password_guidance = PASSWORD_GUIDANCE,
    )


@APP.route("/login", methods=("POST", "GET"))
def log_in_route():
    if "username" in session:
        return redirect("/")
    elif request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            if valid_login_credentials(username, password): 
                session["username"] = username
                session["just_logged_in"] = True
                return redirect("/")

            return render_template(
                "login.html",
                login_guidance = LOGIN_GUIDANCE,
                invalid_credentials = True
            )
        
        except Exception:
            return render_template(
                "login.html",
                login_guidance = LOGIN_GUIDANCE,
                error = True
            )
    
    return render_template(
        "login.html",
        login_guidance = LOGIN_GUIDANCE
    )


@APP.route("/check-username-taken", methods=("POST",))
def username_exists_route():
    with suppress(Exception):
        username = request.get_json()["username"]
        return "1" if username_is_taken(username) else "0"
    return "error"


@APP.route("/account")
def account_route():
    if "username" not in session:
        return redirect("/")
    
    return render_template(
        "account.html",
        username = session["username"],
        just_changed_password = check_for_session_event("just_changed_password")
    )


@APP.route("/log-out")
def log_out_route():
    if "username" in session:
        del session["username"]
        session["just_logged_out"] = True

    return redirect("/") 


@APP.route("/change-password", methods=("POST", "GET"))
def change_password_route():
    if "username" not in session:
        return redirect("/")
    elif request.method == "POST":
        try:
            current_password = request.form["current-password"]
            new_password = request.form["new-password"]
            confirm_new_password = request.form["confirm-new-password"]

            if not valid_change_password_credentials(current_password, new_password, confirm_new_password):
                return render_template(
                    "changepassword.html",
                    username = session["username"],
                    password_guidance = PASSWORD_GUIDANCE,
                    invalid_credentials = True
                )  
            
            elif not password_matches(session["username"], current_password):
                return render_template(
                    "changepassword.html",
                    username = session["username"],
                    password_guidance = PASSWORD_GUIDANCE,
                    incorrect_current_password = True
                )
            
            update_password(session["username"], new_password)
            session["just_changed_password"] = True
            return redirect("/account") 
        
        except Exception:
            return render_template(
                "changepassword.html",
                username = session["username"],
                password_guidance = PASSWORD_GUIDANCE,
                error = True
            )
    
    return render_template(
        "changepassword.html",
        username = session["username"],
        password_guidance = PASSWORD_GUIDANCE
    )


@APP.route("/settings", methods=("POST", "GET"))
def settings_route():
    just_updated_settings = False
    invalid_settings = False
    error = False
    if "username" not in session:
        return redirect("/")
    elif request.method == "POST":
        try:
            form_keys = tuple(request.form.keys())
            languages = [language for language in LANGUAGES if language in form_keys]
            default_langs = {
                "from": request.form["default-from-language-selection"],
                "to": request.form["default-to-language-selection"]       
            }
            character_limit = int(request.form["character-limit"])

            if valid_settings(form_keys, languages, default_langs, character_limit):
                update_settings(session["username"], {
                    "languages": languages,
                    "default_langs": default_langs,
                    "character_limit": character_limit
                })
                just_updated_settings = True
            else:
                invalid_settings = True
        
        except Exception:
            error = True

    current_settings = get_settings(session["username"])
    return render_template(
        "settings.html",
        username = session["username"],
        all_languages = LANGUAGES,
        selected_langs = current_settings["languages"],
        select_languages_guidance = SELECT_LANGUAGES_GUIDANCE,
        default_from = current_settings["default_langs"]["from"],
        default_to = current_settings["default_langs"]["to"],
        default_languages_guidance = DEFAULT_LANGUAGES_GUIDANCE,
        character_limit = current_settings["character_limit"],
        character_limit_guidance = CHARACTER_LIMIT_GUIDANCE,
        just_updated_settings = just_updated_settings,
        just_reset_settings_to_default = check_for_session_event("just_reset_settings_to_default"),
        invalid_settings = invalid_settings,
        error = error
    )


@APP.route("/reset-settings-default")
def reset_settings_to_default_route():
    if "username" not in session:
        return redirect("/")
    
    update_settings(session["username"], DEFAULT_SETTINGS)

    session["just_reset_settings_to_default"] = True
    return redirect("/settings")


@APP.route("/saved-translation-name-exists", methods=("POST",))
def saved_translation_name_exists_route():
    if "username" not in session:
        return redirect("/")

    name = request.get_json()["name"]
    saved_translations = SavedTranslations(session["username"])
    return "1" if saved_translations.name_exists(name) else "0"


@APP.route("/save-translation", methods=("POST",))
def save_translation_route():
    if "username" not in session:
        return redirect("/")

    with suppress(Exception):
        data = request.get_json()
        name = data["name"]
        from_lang = data["from"][18:] if data["from"].startswith("Detect Language") else data["from"]
        source_text = data["source_text"]
        to_lang = data["to"]
        translation = data["translation"]
        name_exists = data["name_exists"]

        if valid_saved_translation(session["username"], name, from_lang, source_text, to_lang, translation, name_exists):
            return SavedTranslations(session["username"]).add(name, from_lang, source_text, to_lang, translation, name_exists)

    return "invalid"


@APP.route("/saved-translations")
def saved_translations_route():
    if "username" not in session:
        return redirect("/")

    saved_translations = SavedTranslations(session["username"])
    return render_template(
        "savedtranslations.html",
        username = session["username"],
        translation_count = len(saved_translations.files),
        kb_used = round(saved_translations.total_size/1024, 2),
        translations = saved_translations.translations,
        additional_data = {file: {
            "source_text_length": len(saved_translations.translations[file]["src_text"]),
            "translation_length": len(saved_translations.translations[file]["translation"]),
            "file_size": round(get_file_size(f"accounts/{session['username']}/saved_translations/{file}")/1024, 2)
        } for file in saved_translations.translations},
        saved_translation_does_not_exist = check_for_session_event("saved_translation_does_not_exist"),
        just_deleted_saved_translation = check_for_session_event("just_deleted_saved_translation"),
        just_deleted_all_saved_translations = check_for_session_event("just_deleted_all_saved_translations")
    )


@APP.route("/saved-translations/<id>")
def specific_saved_translation_route(id: int):
    if "username" not in session:
        return redirect("/")
    
    saved_translations = SavedTranslations(session["username"])
    file = f"{id}.json"
    if file in saved_translations.files:
        translation = saved_translations.translations[file]
        return render_template(
            "savedtranslation.html",
            name = translation["name"],
            from_lang = translation["from"],
            to_lang = translation["to"],
            source_text = translation["src_text"],
            source_text_length = len(translation["src_text"]),
            translation = translation["translation"],
            translation_length = len(translation["translation"]),
            datetime = translation["datetime"],
            file_size = round(get_file_size(f"accounts/{session['username']}/saved_translations/{file}")/1024, 2)
        )
    
    session["saved_translation_does_not_exist"] = True
    return redirect("/saved-translations")


@APP.route("/delete-saved-translation/<id>")
def delete_saved_translation_route(id: int):
    if "username" not in session:
        return redirect("/")
    
    saved_translations = SavedTranslations(session["username"])
    file = f"{id}.json"
    if file in saved_translations.files:
        saved_translations.delete(file)
        session["just_deleted_saved_translation"] = True
    else:
        session["saved_translation_does_not_exist"] = True

    return redirect("/saved-translations")


@APP.route("/delete-all-saved-translations")
def delete_all_saved_translations_route():
    if "username" not in session:
        return redirect("/")
    
    SavedTranslations(session["username"]).delete_all()
    session["just_deleted_all_saved_translations"] = True

    return redirect("/saved-translations")


@APP.route("/help")
def help_route():
    return render_template(
        "help.html",
        username = session.get("username"),
        username_guidance = USERNAME_GUIDANCE,
        password_guidance = PASSWORD_GUIDANCE,
        login_guidance = LOGIN_GUIDANCE,
        select_languages_guidance = SELECT_LANGUAGES_GUIDANCE,
        default_languages_guidance = DEFAULT_LANGUAGES_GUIDANCE,
        character_limit_guidance = CHARACTER_LIMIT_GUIDANCE
    )


@APP.route("/about")
def about_route():
    return render_template(
        "about.html",
        username = session.get("username")
    )


def check_for_session_event(key: str):
    value = session.get(key, False)
    if value:
        del session[key]
    return value 


def translate(from_lang: str, source_text: str, to_lang: str):
    if from_lang == to_lang:
        return {
            "text": source_text,
            "from": attempt_iso_639_1_code_to_language(from_lang)
        }

    translation = Translator().translate(source_text, src=from_lang, dest=to_lang)
    return {
        "text": translation.text,
        "from": attempt_iso_639_1_code_to_language(translation.src)
    }


def attempt_iso_639_1_code_to_language(iso_639_1_code: str):
    iso_639_1_code_lower = iso_639_1_code.lower()
    return next(
        (language for language in LANGUAGES if ISO_639_1_CODES[language] == iso_639_1_code_lower), 
        iso_639_1_code
    )


def update_password(username: str, password: str):
    hash_depth = choice(range(10, 100))
    write_file(f"accounts/{username}/{HASH_DEPTH_FILE}", str(hash_depth).encode(), binary=True)
    hashed_password = hash_string(password, hash_depth).encode()
    write_file(f"accounts/{username}/{PASSWORD_FILE}", hashed_password, binary=True, compress=True)


def update_settings(username: str, settings: dict):
    write_json(f"accounts/{username}/{SETTINGS_FILE}", settings, compress=True)


def get_settings(username: str):
    return read_json(f"accounts/{username}/{SETTINGS_FILE}", is_compressed=True)


if __name__ == "__main__":
    APP.secret_key = "9ba0049e1a296a3e1c9a4dc860f8076843a524a79b0f354dc4c29428ff8d4f14"
    APP.run(port=5001)