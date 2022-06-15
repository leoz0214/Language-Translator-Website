function deleteSavedTranslation() {
    if (confirm("Are you sure you would like to permanently delete this saved translation?")) {
        let parts = String(window.location).split("/");
        window.location = `/delete-saved-translation/${parts[parts.length - 1]}`;
    }
}