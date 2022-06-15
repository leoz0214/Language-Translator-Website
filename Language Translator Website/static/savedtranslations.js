function deleteAllSavedTranslations() {
    if (confirm("Are you sure you would like to delete ALL of your saved translations? This is a big action and cannot be undone.")) {
        window.location = "/delete-all-saved-translations";
    }
}