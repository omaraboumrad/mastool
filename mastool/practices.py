"""
Practices and Checks listing
"""
import ast

from mastool import helpers as h


@h.labeled(code='M001',
           msg='looping against dictionary keys',
           solution="use 'for key in dictionary' instead.")
def find_for_x_in_y_keys(node):
    """Finds looping against dictionary keys"""
    return (
        isinstance(node, ast.For)
        and h.call_name_is(node.iter, 'keys')
    )


@h.labeled(code='M002',
           msg='simplifiable if condition',
           solution="instead of 'if cond: return True else return False' "
                    "use: 'return cond'")
def find_if_x_retbool_else_retbool(node):
    """Finds simplifiable if condition"""
    return (
        isinstance(node, ast.If)
        and isinstance(node.body[0], ast.Return)
        and h.is_boolean(node.body[0].value)
        and h.has_else(node)
        and isinstance(node.orelse[0], ast.Return)
        and h.is_boolean(node.orelse[0].value)
    )


@h.labeled(code='M003',
           msg='joining path with plus',
           solution="instead of: 'p1 + '/' + p2', use 'os.path.join(p1, p2)'")
def find_path_join_using_plus(node):
    """Finds joining path with plus"""
    return (
        isinstance(node, ast.BinOp)
        and isinstance(node.op, ast.Add)
        and isinstance(node.left, ast.BinOp)
        and isinstance(node.left.op, ast.Add)
        and isinstance(node.left.right, ast.Str)
        and node.left.right.s in ['/', "\\"]
    )


@h.labeled(code='M004',
           msg='assigning to built-in',
           solution="change symbol name to something else")
def find_assign_to_builtin(node):
    """Finds assigning to built-ins"""
    builtins = set(__builtins__.keys())

    return (
        isinstance(node, ast.Assign)
        and len(builtins & set(h.target_names(node.targets))) > 0
    )


@h.labeled(code='M005',
           msg='catching a generic exception',
           solution="instead of 'except:' use 'except [Specific]:'")
def find_generic_exception(node):
    """Finds generic exceptions"""
    return (
        isinstance(node, ast.ExceptHandler)
        and node.type is None
    )


@h.labeled(code='M006',
           msg='catching a generic exception and passing it silently',
           solution="instead of 'except: pass' use 'except [Specific]:' "
                    "and handle it")
def find_silent_exception(node):
    """Finds silent generic exceptions"""
    return (
        isinstance(node, ast.ExceptHandler)
        and node.type is None
        and len(node.body) == 1
        and isinstance(node.body[0], ast.Pass)
    )


@h.labeled(code='M007',
           msg='use of import star',
           solution="make explicit imports")
def find_import_star(node):
    """Finds import stars"""
    return (
        isinstance(node, ast.ImportFrom)
        and '*' in h.importfrom_names(node.names)
    )


@h.labeled(code='M008',
           msg='comparing to True or False',
           solution="instead of 'a == True' use 'a' or 'bool(a)'")
def find_equals_true_or_false(node):
    """Finds equals true or false"""
    return (
        isinstance(node, ast.Compare)
        and len(node.ops) == 1
        and isinstance(node.ops[0], ast.Eq)
        and any(h.is_boolean(n) for n in node.comparators)
    )


@h.labeled(code='M009',
           msg='use of list as a default arg',
           solution="instead of 'def foo(a=[])' use "
                    "'def foo(a=None):if not a: a = []'")
def find_default_arg_is_list(node):
    """Finds default args as list"""
    return (
        isinstance(node, ast.FunctionDef)
        and any([n for n in node.args.defaults if isinstance(n, ast.List)])
    )
