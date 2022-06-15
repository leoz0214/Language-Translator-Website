import os 
import json 
import gzip
import shutil
import hashlib


def read_file(file_location: str, binary: bool=False, is_compressed: bool=False, compress_level: int=9):
    if binary:
        if is_compressed:
            with gzip.open(file_location, "rb", compresslevel=compress_level) as f:
                return f.read()
        with open(file_location, "rb") as f:
            return f.read()

    if is_compressed:
        with gzip.open(file_location, "rt", compresslevel=compress_level) as f:
            return f.read()
    with open(file_location, "r", encoding="utf8") as f:
        return f.read()


def write_file(file_location: str, to_write: str, binary: bool=False,
compress: bool=False, compress_level: int=9, replace_existing: bool=True, error_if_exists: bool=False):
    if file_exists(file_location) and not replace_existing:
        if error_if_exists:
            raise FileExistsError("File already exists.")

    elif binary:
        if compress:
            with gzip.open(file_location, "wb", compresslevel=compress_level) as f:
                f.write(to_write)
        else:
            with open(file_location, "wb") as f:
                f.write(to_write)   

    else:
        if compress:
            with gzip.open(file_location, "wt", compresslevel=compress_level, encoding="utf8") as f:
                f.write(to_write)
        else:
            with open(file_location, "w", encoding="utf8") as f:
                f.write(to_write)   


def create_file(file_location: str, replace_existing: bool=True, error_if_exists: bool=False):
    if file_exists(file_location) and not replace_existing:
        if error_if_exists:
            raise FileExistsError("File already exists.")
        return
    with open(file_location, "w", encoding="utf8"):
        return   


def read_json(file_location: str, is_compressed: bool=False, compress_level: int=9):
    if is_compressed:
        with gzip.open(file_location, "rt", compresslevel=compress_level, encoding="utf8") as f:
            return json.load(f)

    with open(file_location, "r", encoding="utf8") as f:
        return json.load(f)


def write_json(file_location: str, to_write, compress: bool=False, compress_level: int=9, replace_existing: bool=True, error_if_exists: bool=False):
    if file_exists(file_location) and not replace_existing:
        if error_if_exists:
            raise FileExistsError("File already exists.")
        return

    if compress:
        with gzip.open(file_location, "wt", compresslevel=compress_level, encoding="utf8") as f:
            json.dump(to_write, f)
    else:
        with open(file_location, "w", encoding="utf8") as f:
            json.dump(to_write, f)


def get_files_in_folder(folder: str):
    return [path for path in os.listdir(folder) if os.path.isfile(f"{folder}/{path}")]


def get_file_size(file_location: str):
    return os.path.getsize(file_location)


def get_total_file_size(file_locations: list):
    return sum(get_file_size(file) for file in file_locations)


def remove_folder(folder: str):
    try:
        shutil.rmtree(folder)
    except Exception as e:
        print(e)


def hash_string(string: str, hash_depth: int=1):
    for i in range(hash_depth):
        string = hashlib.sha512(string.encode()).hexdigest() 
    return string


path_exists = os.path.exists 
folder_exists = os.path.isdir
file_exists = os.path.isfile
create_folder = os.makedirs
remove_file = os.remove
rename = os.rename