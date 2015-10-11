import ast

import helpers as h


@h.labeled('For/In/DictKeys')
def find_for_x_in_y_keys(tree):
    """
    >>> code = '''for x in y.keys():
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_for_x_in_y_keys(tree) == [1]

    >>> code = '''for x in y:
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_for_x_in_y_keys(tree) == []
    """
    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_for(node)
            and h.call_name_is(node.iter, 'keys')
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled('If/RetBool/Else/RetBool')
def find_if_x_ret_bool_else_ret_bool(tree):
    """
    >>> code = '''if foo:
    ...     print True
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_if_x_ret_bool_else_ret_bool(tree) == []

    >>> code = '''if foo:
    ...     return False
    ... else:
    ...     return True
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_if_x_ret_bool_else_ret_bool(tree) == [1]
    """
    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_if(node)
            and h.is_return(node.body[0])
            and h.is_boolean(node.body[0].value)
            and h.has_else(node)
            and h.is_return(node.orelse[0])
            and h.is_boolean(node.orelse[0].value)
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled('JoinPathWithPlus')
def find_path_join_using_plus(tree):
    """
    >>> code = '"a" + "/" + "b"'
    >>> tree = ast.parse(code)
    >>> assert find_path_join_using_plus(tree) == [1]

    >>> code = '''a = "foo"
    ... a + "/" + "b"
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_path_join_using_plus(tree) == [2]

    >>> code = '''a, b = "foo", "bar"
    ... a + "/" + b
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_path_join_using_plus(tree) == [2]
    """
    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_binop(node)
            and h.is_add(node.op)
            and h.is_binop(node.left)
            and h.is_add(node.left.op)
            and h.is_str(node.left.right)
            and node.left.right.s in ['/', "\\"]
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled('AssignToBuiltin')
def find_assign_to_builtin(tree):
    """
    >>> code = 'a = 1'
    >>> tree = ast.parse(code)
    >>> assert find_assign_to_builtin(tree) == []

    >>> code = 'id = 1'
    >>> tree = ast.parse(code)
    >>> assert find_assign_to_builtin(tree) == [1]

    >>> code = 'a, map = 1, 2'
    >>> tree = ast.parse(code)
    >>> assert find_assign_to_builtin(tree) == [1]
    """
    builtins = set(__builtins__.keys())

    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_assign(node)
            and len(builtins & set(h.target_names(node.targets))) > 0
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled('GenericException')
def find_generic_exception(tree):
    """
    >>> code = '''try:
    ...     a
    ... except:
    ...     b
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_generic_exception(tree) == [3]

    >>> code = '''try:
    ...     a
    ... except:
    ...     b
    ... except:
    ...     c
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_generic_exception(tree) == [3, 5]

    >>> code = '''try:
    ...     a
    ... except Exception:
    ...     b
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_generic_exception(tree) == []
    """
    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_except(node)
            and node.type is None
        )

        if checks:
            found.append(node.lineno)

    return found

@h.labeled('SilentGenericException')
def find_silent_exception(tree):
    """
    >>> code = '''try:
    ...     a
    ... except:
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_silent_exception(tree) == [3]

    >>> code = '''try:
    ...     a
    ... except:
    ...     pass
    ... except:
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_silent_exception(tree) == [3, 5]

    >>> code = '''try:
    ...     a
    ... except Exception:
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_silent_exception(tree) == []
    """
    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_except(node)
            and node.type is None
            and len(node.body) == 1
            and h.is_pass(node.body[0])
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled('ImportStar')
def find_import_star(tree):
    """
    >>> code = '''from a import *'''
    >>> tree = ast.parse(code)
    >>> assert find_import_star(tree) == [1]

    >>> code = '''from a import x, y'''
    >>> tree = ast.parse(code)
    >>> assert find_import_star(tree) == []
    """
    found = []

    for node in ast.walk(tree):
        checks = (
            h.is_importfrom(node)
            and '*' in h.importfrom_names(node.names)
        )

        if checks:
            found.append(node.lineno)

    return found
