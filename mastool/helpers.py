"""
helpers to support practices
"""
import ast


def has_else(node):
    """
    Checks if node has else
    """
    return (
        isinstance(node, ast.If)
        and len(node.orelse) > 0
    )


def is_boolean(node):
    """
    Checks if node is True or False
    """
    return (
        isinstance(node, ast.Name)
        and node.id in ('True', 'False')
    )


def call_name_is(siter, name):
    """
    Checks the function call name
    """
    return (
        isinstance(siter, ast.Call)
        and hasattr(siter.func, 'attr')
        and siter.func.attr == name
    )


def target_names(targets):
    """
    Retrieves the target names
    """
    names = []
    for entry in targets:
        if isinstance(entry, ast.Name):
            names.append(entry.id)
        elif isinstance(entry, ast.Tuple):
            for element in entry.elts:
                if isinstance(element, ast.Name):
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
