.. vim: set fileencoding=utf-8:
.. -*- coding: utf-8 -*-
.. +--------------------------------------------------------------------------+
   |                                                                          |
   | Licensed under the Apache License, Version 2.0 (the "License");          |
   | you may not use this file except in compliance with the License.         |
   | You may obtain a copy of the License at                                  |
   |                                                                          |
   |     http://www.apache.org/licenses/LICENSE-2.0                           |
   |                                                                          |
   | Unless required by applicable law or agreed to in writing, software      |
   | distributed under the License is distributed on an "AS IS" BASIS,        |
   | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
   | See the License for the specific language governing permissions and      |
   | limitations under the License.                                           |
   |                                                                          |
   +--------------------------------------------------------------------------+


*******************************************************************************
Release Notes
*******************************************************************************


.. towncrier release notes start


Absence 1.0.1 (2025-01-21)
==========================

Bugfixes
--------

- Convert ``Absential`` to proper type alias and to use separately-declared type
  variable. (Addresses Pyright complaints.)


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
