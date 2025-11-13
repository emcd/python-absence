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
Product Requirements Document
*******************************************************************************

Executive Summary
===============================================================================

The ``absence`` package provides a type-safe, falsey sentinel singleton and
factory for representing absent values in Python code. It addresses the common
pattern where ``None`` is a valid value but developers need to distinguish
"value not provided" from "value provided as None". The package offers a global
``absent`` sentinel, factory for custom sentinels, type predicates, and type
alias support for static type checking.

Problem Statement
===============================================================================

**Who experiences the problem:**
  Python library developers, API designers, and application developers working
  with optional parameters, partial updates, and configuration systems.

**When and where it occurs:**
  - Functions with optional parameters where ``None`` is a valid value
  - Partial update operations (e.g., PATCH APIs, configuration updates)
  - Query builders where absence means "don't filter" vs ``None`` means "filter for NULL"
  - Default value scenarios where ``None`` has semantic meaning

**Impact and consequences:**
  - Developers resort to creating ad-hoc sentinel objects (``_MISSING = object()``)
  - Inconsistent patterns across codebases and libraries
  - Lack of type safety for sentinel detection
  - Verbose code with repeated sentinel creation
  - Potential bugs from truthy sentinel objects in boolean contexts

**Current workarounds and limitations:**

* ``object()`` sentinels: Truthy (confusing in conditionals), not standardized
* ``dataclasses.MISSING``: Truthy, dataclasses-specific, limited scope
* ``typing.NoDefault``: Truthy, typing-specific, Python 3.13+
* PEP 661 sentinel: Still in draft with deferred status, not adopted into Python
* Custom classes: Requires boilerplate in every project

Goals and Objectives
===============================================================================

Primary Objectives
-------------------------------------------------------------------------------

**Provide globally unique absence sentinel (REQ-001)**
  Success metrics:
  - Single ``absent`` instance per Python process
  - Identity checks (``is absent``) work reliably
  - Falsey in boolean contexts

**Enable type-safe absence detection (REQ-002)**
  Success metrics:
  - Type checkers (Pyright, mypy) recognize ``Absential[T]`` type alias
  - Type guards (``is_absent``, ``is_absence``) provide type narrowing
  - Zero false positives in type checking

**Support package-specific sentinels (REQ-003)**
  Success metrics:
  - Factory creates distinct sentinel instances
  - Custom string representations supported
  - Maintains falsey behavior and singleton semantics

Secondary Objectives
-------------------------------------------------------------------------------

**Minimal runtime overhead**
  Success metrics:
  - Sentinel checks compile to identity checks (``is`` operator)
  - No performance penalty vs ``object()`` sentinels
  - Import time under 50ms

**Clear, discoverable API**
  Success metrics:
  - Complete type hints for all public symbols
  - Comprehensive documentation with practical examples
  - Common use cases covered in examples

Target Users
===============================================================================

Python Library Developers
-------------------------------------------------------------------------------

**Technical proficiency:** Advanced Python developers
**Primary needs:**

- Standardized sentinel pattern for library APIs
- Type-safe sentinel detection for better IDE support
- Consistent behavior across different Python versions (3.10+)

**Usage context:** Public library APIs with optional parameters where ``None``
has semantic meaning distinct from "not provided"

API Designers
-------------------------------------------------------------------------------

**Technical proficiency:** Intermediate to advanced
**Primary needs:**

- Clear distinction between "field not included" and "field set to null"
- Type annotations that express optional-but-distinct-from-None semantics
- Minimal cognitive overhead for API consumers

**Usage context:** REST APIs, GraphQL resolvers, configuration systems, database
query builders

Application Developers
-------------------------------------------------------------------------------

**Technical proficiency:** Intermediate
**Primary needs:**

- Simple predicate for checking absence
- Compatible with standard Python patterns (boolean checks, identity checks)
- Clear error messages for misuse

**Usage context:** Business logic with partial updates, optional configurations,
conditional processing

Functional Requirements
===============================================================================

Global Absence Sentinel (Critical)
-------------------------------------------------------------------------------

**REQ-F001: Provide ``absent`` singleton**
  Priority: Critical

  As a Python developer, I want a globally unique ``absent`` sentinel so that I
  can use identity checks to detect absent values reliably.

  Acceptance Criteria:

  - ``absent`` is a module-level singleton
  - ``absent is absent`` evaluates to ``True``
  - ``bool(absent)`` evaluates to ``False``
  - ``str(absent)`` returns ``'absent'``
  - ``repr(absent)`` returns ``'absence.absent'``
  - Multiple imports of ``absent`` reference the same object

**REQ-F002: Prevent sentinel pickling**
  Priority: Critical

  As a library developer, I want absence sentinels to be non-picklable so that
  singleton semantics are guaranteed and bugs from unpickling are prevented.

  Acceptance Criteria:

  - ``pickle.dumps(absent)`` raises ``OperationValidityError``
  - Error message clearly explains why pickling is not supported
  - Behavior is consistent across pickle protocols

Type Safety (Critical)
-------------------------------------------------------------------------------

**REQ-F003: Provide type predicate functions**
  Priority: Critical

  As a Python developer, I want type-safe predicates for checking absence so
  that type checkers can narrow types correctly.

  Acceptance Criteria:

  - ``is_absent(value)`` returns ``True`` only for the global ``absent`` singleton
  - ``is_absence(value)`` returns ``True`` for any ``AbsenceFactory`` instance
  - Both functions are ``TypeIs`` type guards for type checker support
  - Functions work correctly with ``None``, ``False``, and other falsey values

**REQ-F004: Provide ``Absential[T]`` type alias**
  Priority: Critical

  As an API designer, I want a type alias for "value or absent" so that I can
  express optional-but-not-None parameters in type signatures.

  Acceptance Criteria:

  - ``Absential[T]`` is equivalent to ``T | AbsentSingleton``
  - Type checkers recognize ``Absential[int]`` as accepting ``int`` or ``absent``
  - Type narrowing works after ``is_absent()`` checks
  - Supports generic types (e.g., ``Absential[dict[str, Any]]``)

Custom Sentinels (High)
-------------------------------------------------------------------------------

**REQ-F005: Provide ``AbsenceFactory`` for custom sentinels**
  Priority: High

  As a library developer, I want to create package-specific absence sentinels
  so that I can avoid conflicts with the global sentinel in specialized contexts.

  Acceptance Criteria:

  - ``AbsenceFactory()`` creates new sentinel instance
  - Custom ``__repr__`` and ``__str__`` functions supported via parameters
  - All created sentinels are falsey (``bool(sentinel) == False``)
  - Each factory instance is non-picklable
  - ``is_absence(custom_sentinel)`` returns ``True``
  - ``is_absent(custom_sentinel)`` returns ``False``

Builtins Integration (Medium)
-------------------------------------------------------------------------------

**REQ-F006: Provide ``install()`` function for builtins**
  Priority: Medium

  As an application developer, I want to optionally install ``absent`` into
  builtins so that I can use it without imports in frequently-used contexts.

  Acceptance Criteria:

  - ``install()`` with no arguments adds ``Absent`` and ``isabsent`` to builtins
  - Custom names supported via ``sentinel_name`` and ``predicate_name`` parameters
  - ``sentinel_name=None`` skips sentinel installation
  - ``predicate_name=None`` skips predicate installation
  - Multiple calls to ``install()`` with different names do not conflict

Non-Functional Requirements
===============================================================================

Performance Requirements
-------------------------------------------------------------------------------

**REQ-NF001: Minimal runtime overhead**
  - Sentinel identity checks must compile to single ``is`` comparison
  - Import time under 100ms on modern hardware
  - Memory footprint under 10KB for core functionality

**REQ-NF002: Zero cost abstraction for type checking**
  - Type checking should not require runtime overhead
  - ``Absential`` type alias has no runtime cost

Compatibility Requirements
-------------------------------------------------------------------------------

**REQ-NF003: Python version support**
  - Support Python 3.10 and later
  - Use ``typing_extensions`` for backports as needed
  - All features work consistently across supported versions

**REQ-NF004: Type checker compatibility**
  - Full support for Pyright (latest version)
  - Compatible with mypy strict mode
  - Type hints pass validation without errors

Quality Requirements
-------------------------------------------------------------------------------

**REQ-NF005: Code quality standards**
  - 100% test coverage for public API
  - All public symbols have comprehensive docstrings
  - Code passes Ruff linting with project configuration
  - Code passes Pyright type checking in strict mode

**REQ-NF006: API stability**
  - Semantic versioning for all releases
  - Deprecation warnings for API changes (minimum one minor version)
  - No breaking changes in patch releases

Documentation Requirements
-------------------------------------------------------------------------------

**REQ-NF007: Comprehensive documentation**
  - README with quick start and common examples
  - Sphinx documentation with:

    - API reference for all public symbols
    - Usage examples for each feature
    - Comparison with alternatives
    - Migration guides for common patterns

  - Architecture documentation (ADRs, system overview)

Usability Requirements
-------------------------------------------------------------------------------

**REQ-NF008: Developer experience**
  - Clear, actionable error messages for misuse
  - Consistent naming following Python conventions
  - Discoverable via IDE autocomplete
  - Examples cover 90% of common use cases

Constraints and Assumptions
===============================================================================

Technical Constraints
-------------------------------------------------------------------------------

- Depends on ``falsifier`` package for falsey base class
- Depends on ``classcore`` for standard object utilities
- Depends on ``dynadoc`` for documentation annotations
- Python 3.10+ required (for modern type hint syntax)

Design Constraints
-------------------------------------------------------------------------------

- Singleton semantics must be maintained across all code paths
- Falsey behavior is non-negotiable for the sentinel pattern
- Identity-based checks (``is``) are the only reliable detection method
- No pickle support due to singleton requirements (architectural decision)

Assumptions
-------------------------------------------------------------------------------

- Users understand the difference between ``None`` and "absent"
- Type checker usage is common in target user base
- Most use cases involve the global ``absent`` sentinel, not custom factories
- Performance of sentinel checks is critical (hot path usage)

Out of Scope
===============================================================================

The following features are explicitly excluded from this product:

**Pickle/serialization support**
  Pickling absence sentinels would violate singleton semantics. Users must
  handle absence before serialization boundaries.

**Mutable sentinels**
  Sentinels should be immutable to prevent confusion. While complete immutability
  enforcement is a future enhancement, mutable sentinels are not supported.

**Deep integration with standard library**
  This package does not modify ``typing``, ``dataclasses``, or other standard
  library modules. Integration is opt-in via imports.

**Automatic None-to-absent conversion**
  Users must explicitly use ``absent`` vs ``None``. Automatic conversion would
  hide bugs and create confusion.

**Sentinel comparison operations**
  Sentinels do not support ``<``, ``>``, ``<=``, ``>=`` comparisons. Only
  identity (``is``) and equality (``==``) checks are supported.

**Multi-process/distributed uniqueness**
  Singleton guarantees are per-process only. Distributed systems must handle
  absence detection at serialization boundaries.