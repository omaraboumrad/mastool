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
