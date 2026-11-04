import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Загружает метаданные из JSON-файла"""
    try:
        with open (filepath, 'r') as fp:
            return json.load(fp)
    except FileNotFoundError:
        print (f'Файл {filepath} не найден')
        return {}

def save_metadata(filepath, data):
    """Сохраняет метаданные в JSON-файл"""
    with open (filepath, 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)

def load_table_data(table_name):
    """Загружает данные таблицы из папки data/"""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f'{DATA_DIR}/{table_name}.json'
    try:
        with open (filepath, 'r') as fp:
            return json.load(fp)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в папку data/"""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = f'{DATA_DIR}/{table_name}.json'
    with open (filepath, 'w') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)