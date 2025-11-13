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
003. Singleton via __new__ Override
*******************************************************************************

Status
===============================================================================

Accepted

Context
===============================================================================

The global ``absent`` sentinel must be a singleton to enable identity-based
checking via the ``is`` operator. The ``is_absent()`` predicate relies on
``absent is value`` comparisons, which only work reliably if exactly one
instance exists.

Python provides several approaches for implementing singletons:

1. **Module-level instance**: Create instance at module level during import
2. **__new__ override**: Control instance creation in ``__new__`` method
3. **Metaclass**: Use custom metaclass to control class instantiation
4. **Decorator**: Apply singleton decorator to the class
5. **Borg pattern**: Share state between instances rather than identity

The chosen approach must ensure that ``AbsentSingleton()`` always returns the
same instance while maintaining clear, understandable code without excessive
complexity.

Decision
===============================================================================

Implement singleton pattern by overriding ``__new__`` to check for existing
instance in module globals and return it if present, otherwise create new
instance.

Alternatives
===============================================================================

**Module-level instance only (no enforced singleton)**

Rejected because:

- Users could accidentally create ``AbsentSingleton()`` and get different instance
- No protection against breaking identity-based checks
- Requires documentation and convention rather than enforcement
- Subtle bugs if users call constructor instead of using module constant

**Metaclass-based singleton**

Rejected because:

- Adds complexity for functionality that doesn't benefit from metaclass features
- Harder to understand for developers unfamiliar with metaclasses
- Inheritance complications if subclasses needed different behavior
- Overkill for simple singleton requirement

**Singleton decorator**

Rejected because:

- Requires external decorator implementation or dependency
- Adds layer of indirection in class definition
- Less explicit control over singleton behavior
- Decorator pattern less familiar in this context

**Borg pattern (shared state)**

Rejected because:

- Identity checks (``is``) require same object, not shared state
- More complex than needed for immutable sentinel
- Doesn't actually solve the requirement
- Philosophical mismatch with sentinel concept

Consequences
===============================================================================

**Positive:**

- Explicit, self-contained singleton implementation
- No external dependencies or metaclass complexity
- Works naturally with existing inheritance from ``AbsenceFactory``
- Clear control flow in ``__new__`` method
- Prevents accidental creation of multiple instances
- Familiar pattern to Python developers

**Negative:**

- Slightly more complex than module-level constant alone
- ``__new__`` override can be subtle for developers unfamiliar with pattern
- Checks globals on each construction attempt (minor performance cost)
- Does not prevent subclasses from breaking singleton semantics

**Neutral:**

- Standard Python idiom for enforced singletons
- Complements module-level ``absent`` constant
- Balances simplicity with enforcement
