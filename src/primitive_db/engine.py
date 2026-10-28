import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata

db_file = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
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
            metadata = drop_table(metadata, table_name)
            save_metadata(db_file, metadata)
        else:
            print(f'Функции "{command}" нет. Попробуйте снова')
