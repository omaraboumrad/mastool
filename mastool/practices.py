"""
Practices and Checks listing
"""
import ast

from mastool import helpers as h


@h.labeled(code='W001',
           msg='looping against dictionary keys',
           solution="use 'for key in dictionary' instead.")
def find_for_x_in_y_keys(tree):
    """Finds looping against dictionary keys

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
            isinstance(node, ast.For)
            and h.call_name_is(node.iter, 'keys')
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W002',
           msg='simplifiable if condition',
           solution="instead of 'if cond: return True else return False' "
                    "use: 'return cond'")
def find_if_x_retbool_else_retbool(tree):
    """Summary here

    >>> code = '''if foo:
    ...     return True
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_if_x_retbool_else_retbool(tree) == []

    >>> code = '''if foo:
    ...     return False
    ... else:
    ...     return True'''
    >>> tree = ast.parse(code)
    >>> assert find_if_x_retbool_else_retbool(tree) == [1]

    """
    found = []

    for node in ast.walk(tree):
        checks = (
            isinstance(node, ast.If)
            and isinstance(node.body[0], ast.Return)
            and h.is_boolean(node.body[0].value)
            and h.has_else(node)
            and isinstance(node.orelse[0], ast.Return)
            and h.is_boolean(node.orelse[0].value)
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W003',
           msg='joining path with plus',
           solution="instead of: 'p1 + '/' + p2', use 'os.path.join(p1, p2)'")
def find_path_join_using_plus(tree):
    """Finds joining path with plus

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
            isinstance(node, ast.BinOp)
            and isinstance(node.op, ast.Add)
            and isinstance(node.left, ast.BinOp)
            and isinstance(node.left.op, ast.Add)
            and isinstance(node.left.right, ast.Str)
            and node.left.right.s in ['/', "\\"]
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W004',
           msg='assigning to built-in',
           solution="change symbol name to something else")
def find_assign_to_builtin(tree):
    """Finds assigning to built-ins

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
            isinstance(node, ast.Assign)
            and len(builtins & set(h.target_names(node.targets))) > 0
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W005',
           msg='catching a generic exception',
           solution="instead of 'except:' use 'except [Specific]:'")
def find_generic_exception(tree):
    """Finds generic exceptions

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
            isinstance(node, ast.ExceptHandler)
            and node.type is None
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W006',
           msg='catching a generic exception and passing it silently',
           solution="instead of 'except: pass' use 'except [Specific]:' "
                    "and handle it")
def find_silent_exception(tree):
    """Finds silent generic exceptions

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
            isinstance(node, ast.ExceptHandler)
            and node.type is None
            and len(node.body) == 1
            and isinstance(node.body[0], ast.Pass)
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W007',
           msg='use of import star',
           solution="make explicit imports")
def find_import_star(tree):
    """Finds import stars

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
            isinstance(node, ast.ImportFrom)
            and '*' in h.importfrom_names(node.names)
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W008',
           msg='comparing to True or False',
           solution="instead of 'a == True' use 'a' or 'bool(a)'")
def find_equals_true_or_false(tree):
    """Finds equals true or false

    >>> code = '''return a == True'''
    >>> tree = ast.parse(code)
    >>> assert find_equals_true_or_false(tree) == [1]

    >>> code = '''if a == False:
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_equals_true_or_false(tree) == [1]

    >>> code = '''a == b'''
    >>> tree = ast.parse(code)
    >>> assert find_equals_true_or_false(tree) == []

    """
    found = []

    for node in ast.walk(tree):
        checks = (
            isinstance(node, ast.Compare)
            and len(node.ops) == 1
            and isinstance(node.ops[0], ast.Eq)
            and any(h.is_boolean(n) for n in node.comparators)
        )

        if checks:
            found.append(node.lineno)

    return found


@h.labeled(code='W009',
           msg='use of list as a default arg',
           solution="instead of 'def foo(a=[])' use "
                    "'def foo(a=None):if not a: a = []'")
def find_default_arg_is_list(tree):
    """Finds default args as list

    >>> code = '''def foo(x, y):
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_default_arg_is_list(tree) == []

    >>> code = '''def foo(x, y=[]):
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_default_arg_is_list(tree) == [1]

    >>> code = '''def foo(x, y=[1,2,3]):
    ...     pass
    ... '''
    >>> tree = ast.parse(code)
    >>> assert find_default_arg_is_list(tree) == [1]

    """
    found = []

    for node in ast.walk(tree):
        checks = (
            isinstance(node, ast.FunctionDef)
            and any([n for n in node.args.defaults if isinstance(n, ast.List)])
        )

        if checks:
            found.append(node.lineno)

    return found
