"""mastool test module"""

import ast
import collections
import os

from mastool import practices


Fixture = collections.namedtuple('Fixture', 'practice finds ignores')


ALL_FIXTURES = [
    Fixture(
        practice=practices.find_for_x_in_y_keys,
        finds=['for_in_y_keys.py'],
        ignores=['for_in_y.py']
    ),

    Fixture(
        practice=practices.find_if_x_retbool_else_retbool,
        finds=['if_x_bool_else_bool.py'],
        ignores=['if_x_bool.py']
    ),

    Fixture(
        practice=practices.find_path_join_using_plus,
        finds=['path_join.py',
               'path_join_one_var.py',
               'path_join_two_vars.py'],
        ignores=[]
    ),

    Fixture(
        practice=practices.find_assign_to_builtin,
        finds=['assign_builtin.py',
               'assign_builtin_unpack.py'],
        ignores=['no_builtin_assign.py']
    ),

    Fixture(
        practice=practices.find_generic_exception,
        finds=['generic_exception.py',
               'double_generic_exception.py'],
        ignores=['standard_exception.py']
    ),

    Fixture(
        practice=practices.find_silent_exception,
        finds=['generic_silent.py',
               'double_generic_silent.py'],
        ignores=['standard_exception.py']
    ),

    Fixture(
        practice=practices.find_import_star,
        finds=['import_star.py'],
        ignores=['from_import.py']
    ),

    Fixture(
        practice=practices.find_equals_true_or_false,
        finds=['return_equals_bool.py',
               'if_equals_bool.py'],
        ignores=['a_equals_b.py']
    ),

    Fixture(
        practice=practices.find_default_arg_is_list,
        finds=['list_as_arg.py',
               'list_with_vals_as_arg.py'],
        ignores=['function_def.py']
    ),

    Fixture(
        practice=practices.find_if_expression_as_statement,
        finds=['if_expression_as_statement.py'],
        ignores=['if_expression.py']
    ),

    Fixture(
        practice=practices.find_comprehension_as_statement,
        finds=['comprehension_as_statement.py'],
        ignores=['comprehension.py']
    ),

    Fixture(
        practice=practices.find_generator_as_statement,
        finds=['generator_as_statement.py'],
        ignores=['generator.py']
    ),
]


def check(code, practice, assertion):
    """Runs the checker on the code and asserts"""
    tree = ast.parse(code)
    assertion(any(practice(node) for node in ast.walk(tree)))


def finds(result):
    """Positive find callback"""
    assert result


def ignores(result):
    """Negative find callback"""
    assert not result


def samples(path):
    """Samples finder"""
    return os.path.join('mastool/samples', path)


def test_practices():
    """Generates tests using available fixtures"""
    for fixture in ALL_FIXTURES:
        for code in fixture.finds:
            yield check, open(samples(code)).read(), fixture.practice, finds
        for code in fixture.ignores:
            yield check, open(samples(code)).read(), fixture.practice, ignores
