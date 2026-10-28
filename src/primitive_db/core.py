def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует')
        return metadata

    for column in columns:
        if ":" not in column:
            print(f'Некорректное значение: "{column}". Попробуйте снова.')
            return metadata

        column_type = column.split(':', 1)[1]
        if column_type not in ["int", "str", "bool"]:
            print(f'Некорректное значение: "{column}". Попробуйте снова.')
            return metadata

    columns = ['ID:int'] + columns

    metadata[table_name] = {'columns': columns}

    columns_titles = ', '.join(columns)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_titles}')
    return metadata

def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена')
    return metadata