import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    clear_cache,
    create_table,
    delete,
    drop_table,
    insert,
    select,
    update,
)
from primitive_db.parser import parser_set, parser_where
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

db_file = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу\n")
    print("<command> insert into <имя_таблицы> values "
          "(<значение1>, <значение2>, ...) - создать запись")
    print("<command> select from <имя_таблицы> where "
          "<столбец> = <значение> - прочитать записи по условию")
    print("<command> select from <имя_таблицы> - прочитать все записи")    
    print("<command> update <имя_таблицы> set "
          "<столбец1> = <новое_значение1> where "
          "<столбец_условия> = <значение_условия> - обновить запись")
    print("<command> delete from <имя_таблицы> where "
          "<столбец> = <значение> - удалить запись")
    print("<command> info <имя_таблицы> - вывести информацию о таблице\n")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    metadata = load_metadata(db_file)

    print_help()

    while True:
        user_input = prompt.string(">>>Введите команду: ")

        try:
            args = shlex.split(str(user_input))
        except ValueError:
            print(f"Некорректное значение: {user_input}. Попробуйте снова.")
            continue

        if not args:
            continue

        command = args[0]
        args = args[1:]

        if command == "exit":
            print("Выход из программы.")
            break
        
        elif command == "help":
            print_help()
        
        elif command == "list_tables":
            if not metadata:
                print("Список таблиц пуст")
            else:
                for table in metadata:
                    print(f"- {table}")
        
        elif command == "create_table":
            if len(args) < 2:
                print(f"Некорректное значение: {command}. Попробуйте снова.")
                continue
            table_name = args[0]
            columns = args[1:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(db_file, metadata)
        
        elif command == "drop_table":
            if len(args) != 1:
                print(f"Некорректное значение: {args}. Попробуйте снова.")
                continue
            table_name = args[0]
            result = drop_table(metadata, table_name)
            if result is None:
                continue
            metadata = result
            save_metadata(db_file, metadata)
            clear_cache()

        elif command == "insert":
            table_name = args[1]
            values = ' '.join(args[3:])
            values = values.strip('() ')
            values = shlex.split(str(values.replace(", ", " ")))
            if table_name not in metadata:
                print(f"Ошибка: Таблица {table_name} не существует.")
                continue
            data = load_table_data(table_name)
            new_id = max([r['ID'] for r in data], default=0) + 1
            insert_values = insert(metadata, table_name, values)
            if insert_values is not None:
                columns = metadata[table_name]['columns']
                row = {"ID": new_id}
                for col, val in zip(columns[1:], insert_values):
                    col_name, _ = col.split(":")
                    row[col_name] = val
                data.append(row)
                save_table_data(table_name, data)
                clear_cache()
                print(
                    f'Запись с ID={new_id} успешно добавлена ' 
                    f'в таблицу "{table_name}"'
                    )

        elif command == "select":
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            data = load_table_data(table_name)
            where_clause = None
            if 'where' in args:
                where_index = args.index('where')
                condition = " ".join(args[where_index + 1:])
                where_clause = parser_where(condition)
            select_values = select(data, where_clause)
            if not select_values:
                print('Записей не найдено')
                continue
            columns = metadata[table_name]['columns']
            table = PrettyTable()
            table.field_names = [column.split(':')[0] for column in columns]
            for row in select_values:
                table.add_row([row.get(column.split(':')[0], '') for column in columns])
            print(table)

        elif command == "update":
            table_name = args[0]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            data = load_table_data(table_name)
            if 'set' in args:
                condition_set = " ".join(args[2:5])
                set_clause = parser_set(condition_set)
            if 'where' in args:
                condition_where = " ".join(args[6:])
                where_clause = parser_where(condition_where)         
            data, updated_id = update(data, set_clause, where_clause)
            if updated_id is not None:
                save_table_data(table_name, data)
                clear_cache()
                print(
                    f'Запись с ID={updated_id} в таблице "{table_name}" '
                    'успешно обновлена.'
                    )
            else:
                print('Ошибка: Записей для обновления не найдено.')
                    
        elif command == "delete":
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            data = load_table_data(table_name)
            where_clause = None
            if 'where' in args:
                condition_where = " ".join(args[3:])
                where_clause = parser_where(condition_where) 
            result = delete(data, where_clause)      
            if result is None:
                continue
            data, deleted_id = result
            if deleted_id is not None:
                save_table_data(table_name, data)
                clear_cache()
                print(
                    f'Запись с ID={deleted_id} успешно удалена '
                    f'из таблицы "{table_name}".'
                    )
            else:
                print('Ошибка: Записей для удаления не найдено.')

        elif command == "info":
            table_name = args[0]
            if table_name not in metadata:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            data = load_table_data(table_name)
            columns = ", ".join(metadata[table_name]['columns'])
            print(f'Таблица: {table_name}')
            print(f'Столбцы: {columns}')
            print(f'Количество записей: {len(data)}')
        
        else:
            print(f'Функции "{command}" нет. Попробуйте снова')
