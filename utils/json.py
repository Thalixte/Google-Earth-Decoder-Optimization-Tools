import json
import os

from constants import ENCODING


def load_json_file(json_file_path):
    if not os.path.isfile(json_file_path):
        return False

    file = open(json_file_path, encoding=ENCODING)

    try:
        data = json.load(file)
    except:
        data = False
    finally:
        file.close()

    return data


def save_json_file(json_file_path, data):
    if not os.path.isfile(json_file_path):
        return False

    with open(json_file_path, "w") as file:
        file.seek(0)
        json.dump(data, file, indent=4, ensure_ascii=True)
