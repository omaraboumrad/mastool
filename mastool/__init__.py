#! /usr/bin/env python

import sys
import ast

import practices


def main():
    code_file = sys.argv[1]
    try:
        tree = ast.parse(open(code_file).read())
    except SyntaxError:
        print "Error: Could not parse: {}".format(code_file)
        return

    paths = filter(lambda y: hasattr(y, 'label'), practices.__dict__.values())

    for checker in paths:
        adherance = checker(tree)
        for lineno in adherance:
            print '{}:{}: {}'.format(code_file, lineno, checker.label)


if __name__ == '__main__':
    main()
