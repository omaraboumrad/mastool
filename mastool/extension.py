"""Mastool static analysis tool as a Flake8 plugin"""
import ast

from mastool import practices

__version__ = '0.1.3'


class Mastool(object):
    """Flake8 Extension"""

    name = 'mastool'
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree
        self.filename = filename

    @classmethod
    def add_options(cls, parser):
        """Provides the --with-solutions option"""
        parser.add_option('--with-solutions',
                          default=False,
                          action='store',
                          help='Enables mastool possible solutions')

    @classmethod
    def parse_options(cls, options):
        """Assigns the with_solutions option"""
        cls.with_solutions = options.with_solutions

    def build_message(self, checker):
        """Builds the checker's error message to report"""
        solution = ' (%s)' % checker.solution if self.with_solutions else ''
        return '{} {}{}'.format(checker.code,
                                checker.msg,
                                solution)

    def run(self):
        """Primary entry point to the plugin, runs once per file."""
        paths = [x for x in practices.__dict__.values()
                 if hasattr(x, 'code')]

        for node in ast.walk(self.tree):
            try:
                lineno, col_offset = node.lineno, node.col_offset
            except AttributeError:
                # Not all nodes have coordinates, e.g.: ast.Module
                continue

            for checker in paths:
                if checker(node):
                    message = self.build_message(checker)
                    yield lineno, col_offset, message, type(self)
