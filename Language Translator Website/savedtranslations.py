from datetime import datetime

from constants import *
from filehandling import *


class SavedTranslations:

    def __init__(self, username: str):
        self.folder = f"accounts/{username}/saved_translations"
        if not folder_exists(self.folder):
            create_folder(self.folder)
        
        self.files = get_files_in_folder(self.folder)
        self.file_count = len(self.files)
        self.update_total_size()
        self.translations = dict(sorted([(file, read_json(f"{self.folder}/{file}", is_compressed=True)) for file in self.files], 
        key=lambda pair: int(pair[0].split(".")[0]), reverse=True)) # Gets translations in order of creation from most recent.
        self.files = list(self.translations.keys())
    
    def add(self, name: str, from_lang: str, source_text: str, to_lang: str, translated_text: str, name_exists: bool=False):
        if name_exists:
            for file in self.files:
                if name == read_json(f"{self.folder}/{file}", is_compressed=True)["name"]:
                    self.delete(file)
                    break
        
        translation_id = int(self.files[0].split(".")[0]) + 1 if self.files else 0
        file = f"{self.folder}/{translation_id}.json"
        write_json(file, {
            "name": name,
            "from": from_lang,
            "to": to_lang,
            "src_text": source_text,
            "translation": translated_text,
            "datetime": str(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        }, compress=True)

        self.files.insert(0, f"{translation_id}.json")
        self.file_count += 1
        self.update_total_size()
        self.translations[f"{translation_id}.json"] = read_json(file, is_compressed=True)

        if self.total_size > MAX_TOTAL_SAVED_TRANSLATIONS_SIZE:
            self.delete(f"{translation_id}.json")
            self.update_total_size()
            return "size limit exceeded"
        elif self.file_count > MAX_NUMBER_OF_SAVED_TRANSLATIONS:
            self.delete(f"{translation_id}.json")
            self.update_total_size()
            return "file limit exceeded"
        return "success"

    def delete(self, file: str):
        remove_file(f"{self.folder}/{file}")
        self.files.remove(file)
        self.file_count -= 1
        self.update_total_size()
        del self.translations[file]
    
    def delete_all(self):
        for file in self.files.copy():
            self.delete(file)
    
    def update_total_size(self):
        self.total_size = get_total_file_size([f"{self.folder}/{file}" for file in self.files])
    
    def name_exists(self, name: str):
        return any(name == read_json(f"{self.folder}/{file}", is_compressed=True)["name"] for file in self.files)