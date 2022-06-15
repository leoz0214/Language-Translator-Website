window.onbeforeunload = function(event) {
    event.returnValue = "Are you sure you would like to leave the site? Any unsaved changes will be lost."
}


function trackChanges() {
    $(document).on("submit", "form", function() {
        window.onbeforeunload = null;
    });
}


function checkSelectedLanguages() {
    checkLanguageCount();
    checkDefaultLanguages();
}


function getSelectedLanguages() {
    var selectedLanguages = [];
    for (let element of document.getElementsByClassName("settings-language")) {
        if (element.checked) {
            selectedLanguages.push(element.id);
        }
    }
    return selectedLanguages;
}


function checkLanguageCount() {
    const languageCountElement = document.getElementById("language-count");
    var languageCount = getSelectedLanguages().length;
    languageCountElement.innerText = `Languages selected: ${languageCount} / ${languages.length}`;
    if (languageCount < minLanguageCount) {
        languageCountElement.style.color = "red";
        document.getElementById("select-languages-summary").style.color = "red";
        document.getElementById("update-settings").disabled = true;
    } else {
        languageCountElement.style.color = "green";
        document.getElementById("select-languages-summary").style.color = "black";
        document.getElementById("update-settings").disabled = false;
    }
    document.getElementById("select-all-languages").disabled = languageCount === languages.length;
    document.getElementById("deselect-all-languages").disabled = languageCount === 0;
}


function selectAllLanguages() {
    for (let element of document.getElementsByClassName("settings-language")) {
        element.checked = true;
    }
    checkSelectedLanguages();
}


function deselectAllLanguages() {
    for (let element of document.getElementsByClassName("settings-language")) {
        if (element.checked) {
            element.checked = false;
        }
    }
    checkSelectedLanguages();
}


function checkDefaultLanguages() {
    const defaultFromLanguageSelectionElement = document.getElementById("default-from-language-selection");
    const defaultToLanguageSelectionElement = document.getElementById("default-to-language-selection");
    const selectedLanguages = getSelectedLanguages();
    const currentDefaultFromLanguageSelection = defaultFromLanguageSelectionElement.value;
    const currentDefaultToLanguageSelection = defaultToLanguageSelectionElement.value; 
    var defaultFromLanguageSelectionHTML = "";
    var defaultToLanguageSelectionHTML = "";
    var currentDefaultFromLanguageSelectionValid = false;
    var currentDefaultToLanguageSelectionValid = false;

    for (let language of ["Detect Language"].concat(selectedLanguages)) {
        if (language === currentDefaultFromLanguageSelection) {
            defaultFromLanguageSelectionHTML += `<option id="from-${language}" selected}>${language}</option>`;
            currentDefaultFromLanguageSelectionValid = true;
        } else {
            defaultFromLanguageSelectionHTML += `<option id="from-${language}">${language}</option>`; 
        }
        if (language !== "Detect Language"){
            if (language === currentDefaultToLanguageSelection) {
                defaultToLanguageSelectionHTML += `<option id="2to-${language}" selected>${language}</option>`;
                currentDefaultToLanguageSelectionValid = true;
            } else {
                defaultToLanguageSelectionHTML += `<option id="to-${language}">${language}</option>`
            }
        }
    }

    defaultFromLanguageSelectionElement.innerHTML = defaultFromLanguageSelectionHTML;
    defaultToLanguageSelectionElement.innerHTML = defaultToLanguageSelectionHTML;

    if (!currentDefaultFromLanguageSelectionValid) {
        defaultFromLanguageSelectionElement.value = "Detect Language";
    }
    if (!currentDefaultToLanguageSelectionValid) {
        if ("English" in selectedLanguages) {
            defaultToLanguageSelectionElement.value = "English";
        }
    }
}


function resetSettingsToDefault() {
    if (confirm("Are you sure you would like to reset settings to default?")) {
        window.onbeforeunload = null;
        location.href = "/reset-settings-default";
    }
}