var validUsername = false;
var validPassword = false;
var validConfirmPassword = false;


window.onbeforeunload = function(event) {
    if (
        document.getElementById("username").value || 
        document.getElementById("password").value || 
        document.getElementById("confirm-password").value
    ) { // Only warn user if there is any input in the form.
        event.returnValue = "Are you sure you would like to leave the site? The current credentials will be lost.";
    }
}


function trackChanges() {
    $("#username").on("input paste", function() {
        validateUsername();
        validateAllCredentials();
    });

    $("#password, #confirm-password").on("input paste", function() {
        validatePassword();
        validateConfirmPassword();
        validateAllCredentials();
    });

    $(document).on("submit", "form", function() {
        window.onbeforeunload = null;
    });
}


function validateAllCredentials() {
    const submitElement = document.getElementById("sign-up-submit");
    submitElement.disabled = !(validUsername && validPassword && validConfirmPassword);
}


function clearSignUpForm() {
    validUsername = false;
    validPassword = false;
    validConfirmPassword = false;
    document.getElementById("username-status").innerText = "";
    document.getElementById("password-status").innerText = "";
    document.getElementById("confirm-password-status").innerText = "";
    document.getElementById("sign-up-submit").disabled = true;
}


function validateUsername() {
    const username = document.getElementById("username").value;

    if (!username) {
        document.getElementById("username-status").innerText = "";
        validUsername = false;
    } else if (username.length < minUsernameLength) {
        const moreCharactersNeeded = minUsernameLength - username.length;
        if (moreCharactersNeeded === 1) {
            return invalidUsernameProcess(`Username too short, it must be at least ${minUsernameLength} characters long (1 more character needed).`);
        } return invalidUsernameProcess(`Username too short, it must be at least ${minUsernameLength} characters long (${moreCharactersNeeded} more characters needed).`);
    } else if (username.length > maxUsernameLength) {
        const lessCharactersNeeded = username.length - maxUsernameLength;
        if (lessCharactersNeeded === 1) {
            return invalidUsernameProcess(`Username too long, it must be at most ${maxUsernameLength} characters long (1 less character needed).`);
        } return invalidUsernameProcess(`Username too long, it must be at most ${maxUsernameLength} characters long (${lessCharactersNeeded} less characters needed).`);      
    } else if (hasIllegalCharacters(username, legalUsernameCharacters)) {
        invalidUsernameProcess("Username contains illegal characters. Legal username characters: numbers 0-9, letters Aa-Zz, and underscore _");
    } else if (usernameIsTaken(username)) {
        invalidUsernameProcess("Sorry, username is already taken.");
    } else {
        validUsernameProcess();
    }
}


function validUsernameProcess() {
    const usernameStatusElement = document.getElementById("username-status");
    usernameStatusElement.innerText = "Username is valid!";
    usernameStatusElement.style.color = "green";
    validUsername = true;
}


function invalidUsernameProcess(message) {
    const usernameStatusElement = document.getElementById("username-status");
    usernameStatusElement.innerText = message;
    usernameStatusElement.style.color = "red";
    validUsername = false;
}


function usernameIsTaken(username) {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        // Wait for request to complete before exiting function, or nothing will be returned.
        requestComplete = true;
    }

    var requestComplete = false;
    xhttp.open("POST", "/check-username-taken", false);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify({
        "username": username
    }));

    while (!requestComplete) {} // Not great, but will do for now.
    return xhttp.responseText === "1";
}


function validatePassword() {
    const password = document.getElementById("password").value;

    if (!password) {
        document.getElementById("password-status").innerText = "";
        validPassword = false;
    } else if (password.length < minPasswordLength) {
        const moreCharactersNeeded = minPasswordLength - password.length;
        if (moreCharactersNeeded === 1) {
            return invalidPasswordProcess(`Password too short, it must be at least ${minPasswordLength} characters long (1 more character needed).`);
        } return invalidPasswordProcess(`Password too short, it must be at least ${minPasswordLength} characters long (${moreCharactersNeeded} more characters needed).`);
    } else if (password.length > maxPasswordLength) {
        const lessCharactersNeeded = password.length - maxPasswordLength;
        if (lessCharactersNeeded === 1) {
            return invalidPasswordProcess(`Password too long, it must be at most ${maxPasswordLength} characters long (1 less character needed).`);
        } return invalidPasswordProcess(`Password too long, it must be at most ${maxPasswordLength} characters long (${lessCharactersNeeded} less characters needed).`); 
    } else if (hasIllegalCharacters(password, legalPasswordCharacters)) {
        invalidPasswordProcess("Password has illegal characters. Legal characters: numbers 0-9, letters Aa-Zz, spaces, and symbols !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~");
    } else {
        validPasswordProcess();
    }
}


function validPasswordProcess() {
    const passwordStatusElement = document.getElementById("password-status");
    passwordStatusElement.innerText = "Password is valid!";
    passwordStatusElement.style.color = "green";
    validPassword = true;
}


function invalidPasswordProcess(message) {
    const passwordStatusElement = document.getElementById("password-status");
    passwordStatusElement.innerText = message;
    passwordStatusElement.style.color = "red";
    validPassword = false;
}


function validateConfirmPassword() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const confirmPasswordStatusElement = document.getElementById("confirm-password-status");

    if (!confirmPassword) {
        confirmPasswordStatusElement.innerText = "";
        validConfirmPassword = false;
    } else if (confirmPassword !== password) {
        confirmPasswordStatusElement.innerText = "Does not match password.";
        confirmPasswordStatusElement.style.color = "red";
        validConfirmPassword = false;
    } else {
        confirmPasswordStatusElement.innerText = "Matches password.";
        confirmPasswordStatusElement.style.color = document.getElementById("password-status").style.color;
        validConfirmPassword = true;
    }
}