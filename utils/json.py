import json
import os


def load_json_file(json_file_path):
    if not os.path.isfile(json_file_path):
        return False

    file = open(json_file_path)

    try:
        data = json.load(open(json_file_path))
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
