#! /usr/bin/env python
"""
main entry to the tool
"""

from __future__ import print_function

import sys
import ast
import argparse

from mastool import practices


def build_parser():
    """
    Builds the argument parser.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE',
                        help='Target file to run mastool against')

    parser.add_argument('--fail-hard', '-f',
                        dest='fail_hard',
                        action='store_true',
                        default=False,
                        help='exits with a none-zero status when issues found')

    return parser


def main():
    """
    Primary entry point to the tool.
    """
    args = build_parser().parse_args()
    code_file = args.FILE

    try:
        tree = ast.parse(open(code_file).read())
    except SyntaxError:
        print("Error: Could not parse: {}".format(code_file))
        return

    paths = [x for x in practices.__dict__.values() if hasattr(x, 'label')]

    caught = []
    for checker in paths:
        adherance = checker(tree)
        caught.append(len(adherance) > 0)
        for lineno in adherance:
            print('{}:{}: {}'.format(code_file, lineno, checker.label))

    if any(caught) and args.fail_hard:
        sys.exit(1)


if __name__ == '__main__':
    main()
