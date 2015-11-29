[![Build Status](https://travis-ci.org/omaraboumrad/mastool.svg?branch=master)](https://travis-ci.org/omaraboumrad/mastool)

# mastool

static analysis for bad and/or avoidable practices

### Installation

mastool is available on pypi, you can install from source or simply:

    pip install mastool

### Usage

After installing mastool, flake8 would get equipped with mastool's checks.

    $ flake8 [PATH]

Mastool also adds the following switch to flake8, which provides a quick
suggestion about what to replace the reported code with.

    $ flake8 --with-solutions

### Checks

See [here](https://github.com/omaraboumrad/mastool/wiki/Practices) for more details or the summary below.

Code | Message
--- | ---
M001 | looping against dictionary keys
M002 | simplifiable if condition
M003 | joining path with plus
M004 | assigning to built-in
M005 | catching a generic exception
M006 | catching a generic exception and passing it silently
M007 | use of import star
M008 | comparing to True or False
M009 | use of list as a default arg

---

### FAQ

1. Some of these issues are not bad/erroneous!

    Yes, in various contexts sometimes it may be ok (and possibly unavoidable) to
    use these constructs, at which point you can ignore them using Flake8's [config](http://flake8.readthedocs.org/en/latest/config.html)
    mechanism

2. Why did this tool become as a Flake8 extension?

    Flake8 provides a magnificent base for static analysis, there's no point
    in reinventing the wheel.

3. What are some other similar tools?

    You can find some informatin about the subject on my [blog](http://aboumrad.info/essential-python-tools-quality.html)
