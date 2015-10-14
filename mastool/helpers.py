"""
helpers to support practices
"""
import ast


def is_if(node):
    """
    Checks if node is IF
    """
    return isinstance(node, ast.If)


def is_for(node):
    """
    Checks if node is FOR
    """
    return isinstance(node, ast.For)


def is_call(node):
    """
    Checks if node is Call
    """
    return isinstance(node, ast.Call)


def has_else(node):
    """
    Checks if node has else
    """
    return is_if(node) and len(node.orelse) > 0


def is_return(node):
    """
    Checks if node is return
    """
    return isinstance(node, ast.Return)


def is_name(node):
    """
    Checks if node is Name
    """
    return isinstance(node, ast.Name)


def is_boolean(node):
    """
    Checks if node is True or False
    """
    return is_name(node) and node.id in ('True', 'False')

def is_binop(node):
    """
    Checks if node is BinOp
    """
    return isinstance(node, ast.BinOp)


def is_str(node):
    """
    Checks if node is Str
    """
    return isinstance(node, ast.Str)


def is_add(node):
    """
    Checks if node is Add
    """
    return isinstance(node, ast.Add)


def is_assign(node):
    """
    Checks if node is Assign
    """
    return isinstance(node, ast.Assign)


def is_tuple(node):
    """
    Checks if node is Tuple
    """
    return isinstance(node, ast.Tuple)


def is_except(node):
    """
    Checks if node is ExceptHandler
    """
    return isinstance(node, ast.ExceptHandler)


def is_pass(node):
    """
    Checks if node is Pass
    """
    return isinstance(node, ast.Pass)


def is_importfrom(node):
    """
    Checks if node is ImportFrom
    """
    return isinstance(node, ast.ImportFrom)


def is_compare(node):
    """
    Checks if node is Compare
    """
    return isinstance(node, ast.Compare)


def is_eq(node):
    """
    Checks if node is Eq
    """
    return isinstance(node, ast.Eq)


def call_name_is(siter, name):
    """
    Checks the function call name
    """
    return (
        is_call(siter)
        and hasattr(siter.func, 'attr')
        and siter.func.attr == name
    )


def target_names(targets):
    """
    Retrieves the target names
    """
    names = []
    for entry in targets:
        if is_name(entry):
            names.append(entry.id)
        elif is_tuple(entry):
            for element in entry.elts:
                if is_name(element):
                    names.append(element.id)

    return names


def importfrom_names(names):
    """
    Retrieves the importfrom names
    """
    return [n.name for n in names]



def labeled(text):
    """
    decorator to give practices labels
    """
    def for_practice(practice):
        """
        assigns label to practice
        """
        practice.label = text
        return practice
    return for_practice
