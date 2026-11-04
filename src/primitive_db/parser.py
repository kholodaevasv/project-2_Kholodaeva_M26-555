def parser_where(condition):
    """Преобразует строку условия в словарь"""
    if "=" not in condition:
        return None
    
    key, value = condition.split('=')
    key = key.strip()
    value = value.strip()

    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.startswith('"') and value.endswith('"'):
        value = value.strip('"')
    elif value.startswith("'") and value.endswith("'"):
        value = value.strip("'")
    elif value.isdigit():
        value = int(value)

    return {key: value}

def parser_set(condition):
    """Преобразует строку обновления в словарь"""
    return parser_where(condition)