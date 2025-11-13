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
Filesystem Organization
*******************************************************************************

This document describes the specific filesystem organization for the project,
showing how the standard organizational patterns are implemented for this
project's configuration. For the underlying principles and rationale behind
these patterns, see the `common architecture documentation
<https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/architecture.rst>`_.

Project Structure
===============================================================================

Root Directory Organization
-------------------------------------------------------------------------------

The project implements the standard filesystem organization:

.. code-block::

    python-absence/
    ├── LICENSE.txt              # Project license
    ├── README.rst               # Project overview and quick start
    ├── pyproject.toml           # Python packaging and tool configuration
    ├── documentation/           # Sphinx documentation source
    ├── sources/                 # All source code
    ├── tests/                   # Test suites
    └── .auxiliary/              # Development workspace

Source Code Organization
===============================================================================

Package Structure
-------------------------------------------------------------------------------

The main Python package follows the standard ``sources/`` directory pattern:

.. code-block::

    sources/
    └── absence/                     # Main Python package
        ├── __/                      # Centralized import hub
        │   ├── __init__.py          # Re-exports core utilities
        │   ├── imports.py           # External library imports
        │   └── nomina.py            # Naming constants and type aliases
        ├── __init__.py              # Package entry point and public API
        ├── exceptions.py            # Exception hierarchy
        ├── installers.py            # Builtins integration
        ├── objects.py               # Sentinel factory and global singleton
        └── py.typed                 # Type checking marker


All package modules use the standard ``__`` import pattern as documented
in the common architecture guide.

Component Integration
===============================================================================

Module Import Flow
-------------------------------------------------------------------------------

The package uses a layered import structure to maintain clean dependencies:

.. code-block::

    Package Initialization Flow:
    1. __/__init__.py imports from __/imports.py and __/nomina.py
    2. exceptions.py imports from __/ (gets common imports)
    3. objects.py imports from __/ and exceptions.py
    4. installers.py imports from __/ and objects.py
    5. __init__.py imports from all modules and creates public API

Dependency Graph
-------------------------------------------------------------------------------

The flat module structure maintains clear, acyclic dependencies:

.. code-block::

    __/imports.py  ──┐
                     ├──> __/__init__.py ──┐
    __/nomina.py ────┘                     │
                                           ├──> exceptions.py ──┐
                                           │                    │
    falsifier ─────────────────────────────┼────────────────────┼──> objects.py ──┐
                                           │                    │                  │
                                           │                    │                  ├──> installers.py
                                           │                    │                  │
                                           └────────────────────┴──────────────────┴──> __init__.py
                                                                                         (public API)

Import Pattern Benefits
-------------------------------------------------------------------------------

**Centralized External Dependencies**
  All external library imports (``classcore``, ``dynadoc``, ``typing_extensions``)
  are centralized in ``__/imports.py``, making dependency management explicit
  and version upgrades easier.

**No Circular Dependencies**
  The strict layering (``__/`` → ``exceptions`` → ``objects`` → ``installers``
  → ``__init__``) prevents circular import issues and makes the dependency
  graph easy to understand.

**Consistent Import Interface**
  All modules use ``from . import __`` regardless of their position in the
  package, providing a consistent and predictable pattern.

Testing Integration
-------------------------------------------------------------------------------

The test suite mirrors the source structure:

.. code-block::

    tests/
    ├── test_000_imports.py          # Import validation and structure tests
    ├── test_100_exceptions.py       # Exception hierarchy tests
    ├── test_200_objects.py          # Sentinel factory and singleton tests
    └── test_300_installers.py       # Builtins integration tests

Each test module corresponds to a source module and uses numbered functions
(e.g., ``test_201_absent_singleton_identity``) for systematic coverage tracking.

Architecture Evolution
===============================================================================

Current Architecture Constraints
-------------------------------------------------------------------------------

The package is intentionally kept simple with a flat module structure because:

**Single Responsibility**
  The package has one focused purpose: providing absence sentinels. This does
  not require subpackage organization.

**Minimal Dependencies**
  Only four modules provide the complete feature set, making subpackages
  unnecessary overhead. The package maintains a small dependency footprint
  to remain lightweight and focused.

**API Stability**
  A flat structure makes API stability easier to maintain and reduces the
  chance of breaking changes from restructuring.

Evolutionary Principles
-------------------------------------------------------------------------------

**Maintain Backward Compatibility**
  Public API at ``absence.*`` namespace must remain stable. Internal
  reorganization should not affect user imports.

**Resist Premature Optimization**
  Keep the flat structure until concrete needs justify added complexity.
  Each additional level of organization has cognitive cost.

**Preserve Small Footprint**
  The package intentionally avoids integrations with large frameworks or
  libraries to maintain minimal dependencies. Users can build their own
  integrations as needed.

**Document Decisions**
  Any structural changes should be documented via ADRs to preserve the
  rationale for future maintainers.

Reference Documentation
-------------------------------------------------------------------------------

For questions about organizational principles, subpackage patterns, or testing
strategies, refer to the comprehensive common documentation:

* `Architecture Patterns <https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/architecture.rst>`_
* `Development Practices <https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/practices.rst>`_
* `Test Development Guidelines <https://raw.githubusercontent.com/emcd/python-project-common/refs/tags/docs-1/documentation/common/tests.rst>`_
