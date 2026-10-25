import ast


def extract_functions(filepath):
    """Возвращает список функций верхнего уровня из Python-файла.

    Вложенные функции не включаются отдельно — их код и так попадает
    в ast.unparse родительской функции. Поддерживаются async-функции
    и методы классов.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    functions = []
    for node in _iter_functions(tree):
        functions.append({
            "name": node.name,
            "code": ast.unparse(node),
        })

    return functions


def _is_function(node):
    return isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))


def _iter_functions(node):
    """Обходит дерево, отдавая функции, не вложенные в другие функции."""
    for child in ast.iter_child_nodes(node):
        if _is_function(child):
            yield child
        else:
            yield from _iter_functions(child)
