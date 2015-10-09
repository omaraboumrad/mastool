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

## FAQ

How do I make the script return a none-0 code when any result found?

    $ mastool --fail-hard code.py
