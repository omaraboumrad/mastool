[![Build Status](https://travis-ci.org/omaraboumrad/mastool.svg?branch=master)](https://travis-ci.org/omaraboumrad/mastool)

# mastool

static analysis for bad and/or avoidable practices

### Installation

    pip install mastool

### Usage

    usage: mastool [-h] [--verbove] [--fail-hard] TARGET

    positional arguments:
      TARGET           Target file or folder to run mastool against

    optional arguments:
      -h, --help       show this help message and exit
      --verbove, -v    enable suggested solution
      --fail-hard, -f  exits with a none-zero status when issues found

### Checks For

Code | Message
--- | ---
M001 | looping against dictionary keys

    for x in d.keys():
        ...

Code | Message
--- | ---
M002 | simplifiable if condition

    if cond:
        return True
    else:
        return False

Code | Message
--- | ---
M003 | joining path with plus

    path1 + '/' + path2

Code | Message
--- | ---
M004 | assigning to built-in

    id = 1

Code | Message
--- | ---
M005 | catching a generic exception

    try:
        xyz
    except:
        abc

Code | Message
--- | ---
M006 | catching a generic exception and passing it silently

    try:
        xyz
    except:
        pass

Code | Message
--- | ---
M007 | use of import star

    from a import *

Code | Message
--- | ---
M008 | comparing to True or False

    a == True

Code | Message
--- | ---
M009 | use of list as a default arg

    def foo(x, y=[]):
        pass

---

### FAQ

1. Some of these issues are not bad/erroneous!

    Yes, in various contexts sometimes it may be ok (and possibly unavoidable) to
    use these constructs, at which point you can ignore them. (Soon)

2. How do I make the script return a none-0 code when any result found?

    $ mastool --fail-hard code.py

3. How do I show the suggested practice?

    $ mastool --verbose code.py

4. How can I make mastool ignore an entire line?

    add a `# noqa` comment at the end of the line.
