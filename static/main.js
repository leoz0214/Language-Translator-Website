function hasIllegalCharacters(string, legalCharacters) {
    for (let char of string) {
        if (!legalCharacters.includes(char)) {
            return true;
        }
    } return false;
}


function copyText(text) {
    navigator.clipboard.writeText(text);
}