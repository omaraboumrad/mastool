#! /usr/bin/env python
"""main entry to the tool
"""

from __future__ import print_function

import argparse
import ast
import fnmatch
import os
import sys

from mastool import practices


def build_parser():
    """Builds the argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('TARGET',
                        help='Target file or folder to run mastool against')

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


def fetch_files_matching(target, pattern):
    """Retrieve all files from target directory"""
    for root, _, files in os.walk(target):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(root, filename)


def run_checks(node, paths, code_file, verbose):
    """Runs all available checks against node"""
    caught = False
    for checker in paths:
        if checker(node):
            caught = True
            solution = ' (%s)' % checker.solution if verbose else ''
            print('{}:{}: {} {}{}'.format(code_file,
                                          node.lineno,
                                          checker.code,
                                          checker.msg,
                                          solution))
    return caught


def main():
    """Primary entry point to the tool."""
    args = build_parser().parse_args()

    if os.path.isdir(args.TARGET):
        files = fetch_files_matching(args.TARGET, '*.py')
    else:
        files = [args.TARGET]

    caught = []

    for code_file in files:
        try:
            tree = ast.parse(open(code_file).read())
        except SyntaxError:
            print("Error: Could not parse: {}".format(code_file))
            continue

        paths = [x for x in practices.__dict__.values() if hasattr(x, 'code')]

        for node in ast.walk(tree):
            caught.append(run_checks(node, paths, code_file, args.verbose))

    if caught and args.fail_hard:
        sys.exit(1)


if __name__ == '__main__':
    main()
