# mastool

static analysis for bad and/or avoidable practices

## Installation

    pip install mastool

## Usage

    $ mastool code.py

## Checks For

IF/RETURN/BOOL/ELSE/RETURN/BOOL

    if XXX:
        return BOOL
    else:
        return BOOL

FOR/X/IN/DICT/KEYS

    for x in d.keys():
        ...

PATH JOINING WITH PLUS

    a + '/' + b

ASSIGNING TO BUILTIN

    id = 1

GENERIC EXCEPTIONS

    try:
        xyz
    except:
        abc

SILENT GENERIC EXCEPTIONS

    try:
        xyz
    except:
        pass

IMPORT STAR

    from a import *

EQUALS TRUE/FALSE

    a == True

## FAQ

How do I make the script return a none-0 code when any result found?

    $ mastool --fail-hard code.py
