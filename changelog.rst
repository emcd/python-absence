

.. towncrier release notes start

Absence 1.0 (2024-12-20)
========================

Features
--------

- Add ``AbsenceFactory`` class for creating package-specific absence sentinels.
  Each instance evaluates to ``False`` in boolean contexts, has unique identity,
  and supports customizable string representations.
- Add ``Absential`` type alias for annotating values that may be absent,
  supporting clear type hints for optional parameters and return values where
  ``None`` is a valid value.
- Add ``absent`` sentinel, a falsey singleton that represents absence in contexts
  where ``None`` might be a valid value. The sentinel maintains global uniqueness,
  supports proper equality comparison, and can be installed as a builtin.
- Add ``is_absent`` and ``is_absence`` predicates for type-safe checking of
  absence sentinels. These can distinguish between the global sentinel and
  factory-produced sentinels, and support installation as builtins.
- Add optional builtin installation support, allowing the ``absent`` sentinel
  and its predicates to be used without imports, similar to ``None``. Supports
  custom names and selective installation of components.


Supported Platforms
-------------------

- Add support for CPython 3.10 to 3.13.
- Add support for PyPy 3.10.
