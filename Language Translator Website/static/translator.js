var lastSourceText = null;
var currentlyTranslating = false;
var waiting = false;
var waitEvent = null;


window.onbeforeunload = function(event) {
    if (document.getElementById("src-text").value) { // Only warn user if translation is not empty.
        event.returnValue = "Are you sure you would like to leave the site? The current translation will be lost.";
    }
}


function trackChanges() {
    $("#src-text").on("input paste", function() {
        tryToTranslate();
    });

    $("#new-saved-translation-name").on("input paste", function() {
        validateNewSavedTranslationName();
    })
}


function tryToTranslate(fromEvent=false, languageChanged=false) {
    const sourceTextElement = document.getElementById("src-text");
    const characterCountElement = document.getElementById("character-count");
    const sourceText = sourceTextElement.value;
    const textLength = sourceText.length;
    const trimmedText = sourceText.trim();

    if (textLength > maxSourceTextInputLength) {
        sourceTextElement.value = sourceText.slice(0, maxSourceTextInputLength);
        characterCountElement.innerText = `Character count: ${maxSourceTextInputLength} / ${maxSourceTextLength}`;
    } else {
        characterCountElement.innerText = `Character count: ${textLength} / ${maxSourceTextLength}`;
        characterCountElement.style.color = textLength > maxSourceTextLength ? "red" : 
                                            textLength >= maxSourceTextLength * 0.75 ? "orange" : 
                                            textLength >= maxSourceTextLength * 0.5 ? "yellowgreen" : 
                                            textLength === 0 ? "black" : "green";
    }

    if (currentlyTranslating || (waiting && !fromEvent)) {
        if (!waitEvent) {
            waitEvent = setInterval(function() {
                tryToTranslate(true, languageChanged);
            }, 1000); // Minimises requests to 1 per second. Reduces load on server.
            waiting = true;
        }
        return;
    } else if (waitEvent) {
        clearInterval(waitEvent);
        waitEvent = null;
        waiting = false;
    }

    if (trimmedText !== lastSourceText || languageChanged) {
        translate(trimmedText, textLength);
    }
}


function translate(text, textLength) {
    const fromLangElement = document.getElementById("from-lang");
    const translatedTextElement = document.getElementById("translated-text");
    const clearSourceTextElement = document.getElementById("clear-source-text");
    const copyTranslationElement = document.getElementById("copy-translation");
    const saveTranslationElement = document.getElementById("open-save-translation-button") // Null if not logged in.
    const invertLanguagesElement = document.getElementById("invert-languages");
    currentlyTranslating = true;

    if (!text) { // Empty translation.
        translatedTextElement.innerText = "";
        translatedTextElement.style.color = "black";
        clearSourceTextElement.disabled = true;
        copyTranslationElement.disabled = true;
        if (saveTranslationElement) {
            saveTranslationElement.disabled = true;
        }
        lastSourceText = "";
        if (fromLangElement.innerText.startsWith("Detect Language")) {
            fromLangElement.innerText = "Detect Language";
            invertLanguagesElement.disabled = true;
        } else {
            invertLanguagesElement.disabled = !(selectedLanguages.includes(fromLangElement.innerText));
        }
        currentlyTranslating = false;
        return;
    } else if (textLength > maxSourceTextLength) { // Translation too long.
        translatedTextElement.innerText = "Too many characters.";
        translatedTextElement.style.color = "red";
        clearSourceTextElement.disabled = false;
        copyTranslationElement.disabled = true;
        if (saveTranslationElement) {
            saveTranslationElement.disabled = true;
        }
        invertLanguagesElement.disabled = true;
        lastSourceText = text;
        if (fromLangElement.innerText.startsWith("Detect Language")) {
            fromLangElement.innerText = "Detect Language";
        }
        currentlyTranslating = false;
        return;
    }
    // Ajax to get translation from web server (Flask).
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const response = JSON.parse(xhttp.responseText);
        translatedTextElement.innerText = response["text"];
        translatedTextElement.style.color = "black";
        clearSourceTextElement.disabled = false;
        copyTranslationElement.disabled = false;
        if (saveTranslationElement) {
            saveTranslationElement.disabled = false;
        }
        lastSourceText = text;
        if (fromLangElement.innerText.startsWith("Detect Language")) {
            fromLangElement.innerText = `Detect Language - ${response["from"]}`;
        }
        const fromLanguageIncluded = selectedLanguages.includes(response["from"]);
        invertLanguagesElement.disabled = !fromLanguageIncluded;
        if (saveTranslationElement) {
            saveTranslationElement.disabled = !fromLanguageIncluded;
        }
        currentlyTranslating = false;
    }
    
    translatedTextElement.style.color = "grey";
    xhttp.open("POST", "/translator", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify({
        "from_lang": fromLangElement.innerText,
        "source_text": text,
        "to_lang": document.getElementById("to-lang").innerText
    }));
}


function showOrHide(element, keepSpace=false) {
    if (keepSpace) {
        element.style.visibility = (element.style.visibility === "hidden") ? "visible" : "hidden";
    } else {
        element.hidden = !element.hidden;
    }
}


function configFromLanguagesSelection() {
    const element = document.getElementById("from-lang-selection");
    showOrHide(element, true);
    element.setAttribute("value", document.getElementById("from-lang").innerText);
}


function configToLanguagesSelection() {
    const element = document.getElementById("to-lang-selection");
    showOrHide(element, true);
    element.setAttribute("value", document.getElementById("to-lang").innerText);
}


function changeFromLanguage() {
    const newFromLanguage = document.getElementById("from-lang-selection").value;
    document.getElementById("from-lang").innerText = newFromLanguage;
    tryToTranslate(true, true);
    configFromLanguagesSelection();
}


function changeToLanguage() {
    const newToLanguage = document.getElementById("to-lang-selection").value;
    document.getElementById("to-lang").innerText = newToLanguage;
    tryToTranslate(true, true);
    configToLanguagesSelection();
}


function clearSourceText() {
    document.getElementById("src-text").value = "";
    tryToTranslate(true);
}


function copyTranslation() {
    copyText(document.getElementById("translated-text").innerText);
}


function invertLanguages() {
    const fromLangElement = document.getElementById("from-lang");
    const currentFromLang = fromLangElement.innerText.startsWith("Detect Language") ? fromLangElement.innerText.slice(18) : fromLangElement.innerText;
    const toLangElement = document.getElementById("to-lang");
    const currentToLang = toLangElement.innerText;
    const currentTranslatedText = document.getElementById("translated-text").innerText;

    fromLangElement.innerText = currentToLang;
    toLangElement.innerText = currentFromLang;
    document.getElementById("src-text").value = currentTranslatedText;

    document.getElementById("from-lang-selection").value = currentToLang;
    document.getElementById("to-lang-selection").value = currentFromLang;

    tryToTranslate(true, true);
}


function checkNewSavedTranslationNameExistence() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        if (xhttp.responseText === "1" && (!confirm("The specified name for this saved translation is already in use. Would you like to replace it?"))) {
            return;
        } else {
            saveTranslation(xhttp.responseText === "1");
        }
    }

    xhttp.open("POST", "/saved-translation-name-exists", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify({
        "name": document.getElementById("new-saved-translation-name").value
    }));
}


function saveTranslation(nameExists=false) {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const response = xhttp.responseText;
        const saveTranslationElement = document.getElementById("save-translation");
        if (response === "size limit exceeded") {
            saveTranslationElement.style.color = "red";
            saveTranslationElement.innerHTML = `<p>Unfortunately, you do not have enough space left to save this translation.<p>
            <p>Remove some unused saved translations to make space for more.</p>
            <p>The maximum total size of saved translations is 100KB.
            <p>Try to avoid massive translations, particularly ones which are not repetitive. They will eat up space.</p>`
        } else if (response === "file limit exceeded") {
            saveTranslationElement.style.color = "red";
            saveTranslationElement.innerHTML = `<p>Unfortunalately, you have reached the saved translations limit of 256.</p>
            <p>Remove some unused saved translations to make space for more.</p>`
        } else if (response === "invalid") {
            saveTranslationElement.style.color = "red";
            saveTranslationElement.innerHTML = `<p>Something went wrong... if you did not tamper with code, sorry for the inconvenience.
            Otherwise, what did you expect?</p>`
        } else {
            saveTranslationElement.style.color = "green";
            saveTranslationElement.innerHTML = `<p>Successfully saved the translation!</p>`
        }
        saveTranslationElement.innerHTML += `<button onclick='closeSaveTranslationAfterSaveAttempt();'>Close</button>`
    }

    xhttp.open("POST", "/save-translation", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify({
        "name": document.getElementById("new-saved-translation-name").value,
        "from": document.getElementById("from-lang").innerText,
        "source_text": document.getElementById("src-text").value,
        "to": document.getElementById("to-lang").innerText,
        "translation": document.getElementById("translated-text").innerText,
        "name_exists": nameExists
    }));

    document.getElementById("save-translation").innerHTML = `<p>Saving...</p>`;
}


function openSaveTranslation() {
    document.getElementById("save-translation").hidden = false;
}


function clearSaveTranslation() {
    document.getElementById("new-saved-translation-name").value = "";
    validateNewSavedTranslationName();
}


function closeSaveTranslation() {
    document.getElementById("save-translation").hidden = true;
    clearSaveTranslation();
}


function closeSaveTranslationAfterSaveAttempt() {
    const saveTranslationElement = document.getElementById("save-translation");
    saveTranslationElement.hidden = true;
    saveTranslationElement.style.color = "black";
    saveTranslationElement.innerHTML = `<label for="new-saved-translation-name">New saved translation name:</label>
    <input type="text" name="new-saved-translation-name" id="new-saved-translation-name">
    <p id="new-saved-translation-status" hidden></p>
    
    <br>
    <button id="save-translation-button" onclick="checkNewSavedTranslationNameExistence();">Save</button>
    <br>
    <br>
    <button id="clear-save-translation" onclick="clearSaveTranslation();" disabled>Clear</button>
    <br>
    <br>
    <button id="close-save-translation" onclick="closeSaveTranslation();">Close</button>
    <p>Maximum 128 characters. Must not already be a name in use by you.</p>`; // Initial save.

    trackChanges();
}


function validateNewSavedTranslationName() {
    const newSavedTranslationStatus = document.getElementById("new-saved-translation-status");
    const newSavedTranslationName = document.getElementById("new-saved-translation-name").value;

    if (newSavedTranslationName.length > maxNewSavedTranslationNameLength) {
        const lessCharactersNeeded = newSavedTranslationName.length - maxNewSavedTranslationNameLength;
        if (lessCharactersNeeded === 1) {
            newSavedTranslationStatus.innerText = "Too long. 1 less character needed.";
        } else {
            newSavedTranslationStatus.innerText = `Too long. ${lessCharactersNeeded} less characters needed.`;
        }
        newSavedTranslationStatus.hidden = false;
        document.getElementById("save-translation-button").disabled = true;
    } else {
        newSavedTranslationStatus.hidden = true;
        document.getElementById("save-translation-button").disabled = !newSavedTranslationName;
    }

    document.getElementById("clear-save-translation").disabled = !newSavedTranslationName;
}