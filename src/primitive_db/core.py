from decorators import confirm_action, handle_db_errors, log_time


def create_cacher():
    cache = {}
    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        result = value_func()
        cache[key] = result
        return result
    return cache_result

select_cache = create_cacher()   

@handle_db_errors
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

@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена')
    return metadata

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует')
        return None

    columns = metadata[table_name]['columns'][1:]    
    if len(values) != len(columns):
        print('Ошибка: Кол-во переданных значений не соответствует кол-ву столбцов')
        return None

    columns_types = []
    for column in columns:
        column_type = column.split(':', 1)[1]
        columns_types.append(column_type)

    list_values = []
    for val, col_type in zip(values, columns_types):
        if col_type == 'bool':
            if str(val).lower() in ('true', 'false'):
                value = str(val).lower() == 'true'
            else:
                raise ValueError
        elif col_type == 'int':
            value = int(val)
        else:
            value = val

            list_values.append(value)

    return list_values

@handle_db_errors
@log_time
def select(table_data, where_clause=None):

    cache_key = str(where_clause)

    def cache_select():

        if where_clause is None:
            return table_data

        key = list(where_clause.keys())[0]
        value = list(where_clause.values())[0]

        result = []
        for row in table_data:
            row_value = row.get(key)
            if str(row_value).lower() == str(value).lower():
                result.append(row)

        return result

    return select_cache(cache_key, cache_select)

@handle_db_errors
def update(table_data, set_clause, where_clause):
    key_set, value_set = list(set_clause.items())[0]
    key_where, value_where = list(where_clause.items())[0]

    updated_id = None

    for row in table_data:
        row_value = row.get(key_where)
        if str(row_value).lower() == str(value_where).lower():
            row[key_set] = value_set
            updated_id = row.get("ID")

    return table_data, updated_id

@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause):
    key, value = list(where_clause.items())[0]

    deleted_id = None

    result = []
    for row in table_data:
        row_value = row.get(key)
        if str(row_value).lower() != str(value).lower():
            result.append(row)
        else:
            deleted_id = row.get("ID")

    return result, deleted_id