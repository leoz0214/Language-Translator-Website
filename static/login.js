function trackChanges() {
    $("#username").on("input paste", function() {
        const usernameElement = document.getElementById("username");
        const username = usernameElement.value;
        if (username.length > maxLoginUsernameInputLength) {
            usernameElement.value = username.slice(0, maxLoginUsernameInputLength);
        }
    });

    $("#password").on("input paste", function() {
        const passwordElement = document.getElementById("password");
        const password = passwordElement.value;
        if (password.length > maxLoginPasswordInputLength) {
            passwordElement.value = password.slice(0, maxLoginPasswordInputLength);
        }
    });
}