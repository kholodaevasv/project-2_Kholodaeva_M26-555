import json


def load_metadata(filepath):
    try:
        with open (filepath, 'r') as fp:
            return json.load(fp)
    except FileNotFoundError:
        print (f'Файл {filepath} не найден')
        return {}

def save_metadata(filepath, data):
    with open (filepath, 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)