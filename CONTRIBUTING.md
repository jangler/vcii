Contributing to `vcii`
======================

How to contribute
-----------------

The usual "fork & pull" model--just fork the repository, then make a pull
request on [the project's GitHub page](https://github.com/jangler/vcii) when
you're finished making changes. If you just want to report a bug or request a
feature, use the [issue tracker](https://github.com/jangler/vcii/issues).

Coding guidelines
-----------------

`vcii` should depend only on Python 3. No external libraries should be
required--even Python libraries.

Code should pass inspection from [`pep8`](https://pypi.python.org/pypi/pep8)
and [`pylint -E`](https://pypi.python.org/pypi/pylint), and have 100% line and
branch unit test coverage as measured by
[`coverage`](https://pypi.python.org/pypi/coverage). These metrics represent
only minimum standards to which code should comply--just because these tools
approve code doesn't meen it's good, so use common sense!
