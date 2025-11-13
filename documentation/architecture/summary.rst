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
System Overview
*******************************************************************************

The ``absence`` package provides a falsey sentinel singleton and factory for
representing absent values in contexts where ``None`` or ``False`` might be
valid values. This is a focused, single-purpose library designed around
simplicity and type safety.

Major Components
===============================================================================

The system consists of four primary components organized in a flat module
structure:

Sentinel Factory (``objects.py``)
-------------------------------------------------------------------------------

**AbsenceFactory**
  Base class for creating arbitrary absence sentinels. Inherits from
  ``falsifier.Falsifier`` to ensure falsey behavior in boolean contexts.
  Provides customization hooks for ``__repr__`` and ``__str__`` representations.
  Explicitly prevents pickling to maintain singleton semantics.

**AbsentSingleton**
  Specialized subclass implementing the global ``absent`` sentinel using
  singleton pattern. Overrides ``__new__`` to ensure only one instance exists
  per process. Provides fixed string representations.

**Type Utilities**
  - ``is_absence()``: Type guard checking if value is any AbsenceFactory instance
  - ``is_absent()``: Type guard checking if value is the global ``absent`` singleton
  - ``Absential[T]``: Type alias equivalent to ``T | AbsentSingleton``

Builtins Integration (``installers.py``)
-------------------------------------------------------------------------------

**install() function**
  Provides optional installation of ``absent`` sentinel and ``is_absent``
  predicate into Python's builtins module, following naming conventions of
  built-in types (``None``, ``Ellipsis``) and predicates (``isinstance``).
  Supports customizable names for both components.

Exception Hierarchy (``exceptions.py``)
-------------------------------------------------------------------------------

**Omniexception/Omnierror**
  Base exception types integrating with ``classcore`` attribute visibility
  system for consistent exception handling across the package.

**OperationValidityError**
  Raised when invalid operations are attempted (e.g., pickling absence sentinels).

Import Management (``__/`` subpackage)
-------------------------------------------------------------------------------

**Centralized imports hub**
  - ``imports.py``: External library imports (``classcore``, ``dynadoc``, ``typing_extensions``)
  - ``nomina.py``: Common type aliases and package-specific names
  - ``__init__.py``: Re-exports for consistent access via ``from . import __`` pattern

Component Relationships
===============================================================================

The architecture maintains strict separation of concerns:

.. code-block::

    __init__.py
    ├── imports from objects.py
    │   ├── AbsenceFactory (base)
    │   ├── AbsentSingleton (singleton)
    │   ├── absent (global instance)
    │   ├── is_absence() (predicate)
    │   ├── is_absent() (predicate)
    │   └── Absential (type alias)
    ├── imports from installers.py
    │   └── install() (builtins integration)
    └── imports from exceptions.py
        └── exception hierarchy

    All modules depend on __/ for imports
    objects.py depends on exceptions.py and falsifier
    installers.py depends on objects.py
    No circular dependencies

Key Architectural Patterns
===============================================================================

**Singleton Pattern**
  ``AbsentSingleton`` implements singleton via ``__new__`` override,
  ensuring process-wide uniqueness of the ``absent`` sentinel.

**Factory Pattern**
  ``AbsenceFactory`` enables creation of package-specific absence sentinels
  while maintaining consistent behavior.

**Type Safety**
  Type guards (``TypeIs``) and type aliases (``Absential``) provide static
  type checking support for absence detection.

**Inheritance-Based Behavior**
  Falsey behavior inherited from ``falsifier.Falsifier`` rather than
  implemented directly, following composition over duplication.

**Immutability by Convention**
  Absence sentinels prevent pickling and discourage modification, though
  complete immutability is documented as a future enhancement.

Data Flow
===============================================================================

The package has minimal data flow as it primarily provides sentinel values:

1. Package initialization creates the global ``absent`` singleton
2. User code imports ``absent``, predicates, and types
3. User code uses ``absent`` as default values or sentinel markers
4. Predicates check identity (``is``) against sentinels
5. Optional: ``install()`` exposes symbols to builtins namespace

Deployment Architecture
===============================================================================

Pure Python library with no external runtime dependencies beyond:

- ``falsifier``: Provides base falsey object behavior
- ``classcore``: Standard object utilities and attribute management
- ``dynadoc``: Documentation annotation support
- ``typing_extensions``: Modern type hint support

Deployed as a standard Python package via PyPI. No services, daemons, or
persistent state.