#! /usr/bin/env python
"""main entry to the tool
"""

from __future__ import print_function

import argparse
import ast
import sys

from mastool import practices


def build_parser():
    """Builds the argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE',
                        help='Target file to run mastool against')

    parser.add_argument('--verbove', '-v',
                        dest='verbose',
                        action='store_true',
                        default=False,
                        help='enable suggested solution')

    parser.add_argument('--fail-hard', '-f',
                        dest='fail_hard',
                        action='store_true',
                        default=False,
                        help='exits with a none-zero status when issues found')

    return parser


def main():
    """Primary entry point to the tool."""
    args = build_parser().parse_args()
    code_file = args.FILE

    try:
        tree = ast.parse(open(code_file).read())
    except SyntaxError:
        print("Error: Could not parse: {}".format(code_file))
        return

    paths = [x for x in practices.__dict__.values() if hasattr(x, 'code')]

    caught = []
    for checker in paths:
        adherance = checker(tree)
        caught.append(len(adherance) > 0)
        for lineno in adherance:
            solution_text = ' %s' % checker.solution if args.verbose else ''
            print('{}:{}: {} {}{}'.format(code_file,
                                          lineno,
                                          checker.code,
                                          checker.msg,
                                          solution_text))

    if any(caught) and args.fail_hard:
        sys.exit(1)


if __name__ == '__main__':
    main()
