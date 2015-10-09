import ast


is_if = lambda s: isinstance(s, ast.If)
is_for = lambda s: isinstance(s, ast.For)
is_call = lambda s: isinstance(s, ast.Call)
has_else = lambda s: is_if(s) and len(s.orelse) > 0
is_return = lambda s: isinstance(s, ast.Return)
is_name = lambda s: isinstance(s, ast.Name)
is_boolean = lambda n: is_name(n) and n.id in ('True', 'False')
is_binop = lambda s: isinstance(s, ast.BinOp)
is_str = lambda s: isinstance(s, ast.Str)
is_add = lambda s: isinstance(s, ast.Add)


def call_name_is(s, n):
    return (
        is_call(s)
        and hasattr(s.func, 'attr')
        and s.func.attr == n
    )


def labeled(text):
    def for_practice(practice):
        practice.label = text
        return practice
    return for_practice
