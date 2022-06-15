var validNewPassword = false;
var validConfirmNewPassword = false;


window.onbeforeunload = function(event) {
    if (document.getElementById("new-password").value || document.getElementById("confirm-new-password").value) {
        event.returnValue = "Are you sure you would like to leave the site? The current credentials will be lost.";
    }
}


function trackChanges() {
    $("#new-password").on("input paste", function() {
        validateNewPassword();
        validateConfirmNewPassword();
        validateNewPasswordCredentials();
    });

    $("#confirm-new-password").on("input paste", function() {
        validateNewPassword();
        validateConfirmNewPassword();
        validateNewPasswordCredentials();
    });

    $(document).on("submit", "form", function() {
        window.onbeforeunload = null;
    });
}


function validateNewPasswordCredentials() {
    const submitElement = document.getElementById("change-password-submit");
    submitElement.disabled = !(validNewPassword && validConfirmNewPassword);
}


function clearChangePasswordForm() {
    validNewPassword = false;
    validConfirmNewPassword = false;
    document.getElementById("change-password-status").innerText = "";
    document.getElementById("confirm-change-password-status").innerText = "";
    document.getElementById("change-password-submit").disabled = true;
}

function validateNewPassword() {
    const password = document.getElementById("new-password").value;

    if (!password) {
        document.getElementById("new-password-status").innerText = "";
        validNewPassword = false;
    } else if (password === document.getElementById("current-password").value) {
        return invalidNewPasswordProcess("New password must not be the same as your current password.")
    } else if (password.length < minPasswordLength) {
        const moreCharactersNeeded = minPasswordLength - password.length;
        if (moreCharactersNeeded === 1) {
            return invalidNewPasswordProcess(`Password too short, it must be at least ${minPasswordLength} characters long (1 more character needed).`);
        } return invalidNewPasswordProcess(`Password too short, it must be at least ${minPasswordLength} characters long (${moreCharactersNeeded} more characters needed).`);
    } else if (password.length > maxPasswordLength) {
        const lessCharactersNeeded = password.length - maxPasswordLength;
        if (lessCharactersNeeded === 1) {
            return invalidNewPasswordProcess(`Password too long, it must be at most ${maxPasswordLength} characters long (1 less character needed).`);
        } return invalidNewPasswordProcess(`Password too long, it must be at most ${maxPasswordLength} characters long (${lessCharactersNeeded} less characters needed).`); 
    } else if (hasIllegalCharacters(password, legalPasswordCharacters)) {
        invalidNewPasswordProcess("Password has illegal characters. Legal characters: numbers 0-9, letters Aa-Zz, spaces, and symbols !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~");
    } else {
        validNewPasswordProcess();
    }
}


function validNewPasswordProcess() {
    const passwordStatusElement = document.getElementById("new-password-status");
    passwordStatusElement.innerText = "Password is valid!";
    passwordStatusElement.style.color = "green";
    validNewPassword = true;
}


function invalidNewPasswordProcess(message) {
    const passwordStatusElement = document.getElementById("new-password-status");
    passwordStatusElement.innerText = message;
    passwordStatusElement.style.color = "red";
    validNewPassword = false;
}


function validateConfirmNewPassword() {
    const password = document.getElementById("new-password").value;
    const confirmPassword = document.getElementById("confirm-new-password").value;
    const confirmPasswordStatusElement = document.getElementById("confirm-new-password-status");

    if (!confirmPassword) {
        confirmPasswordStatusElement.innerText = "";
        validConfirmNewPassword = false;
    } else if (confirmPassword !== password) {
        confirmPasswordStatusElement.innerText = "Does not match password.";
        confirmPasswordStatusElement.style.color = "red";
        validConfirmNewPassword = false;
    } else {
        confirmPasswordStatusElement.innerText = "Matches password.";
        confirmPasswordStatusElement.style.color = document.getElementById("new-password-status").style.color;
        validConfirmNewPassword = true;
    }
}