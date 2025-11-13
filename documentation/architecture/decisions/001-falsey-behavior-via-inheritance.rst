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
001. Falsey Behavior via Inheritance
*******************************************************************************

Status
===============================================================================

Accepted

Context
===============================================================================

Absence sentinels need to evaluate to ``False`` in boolean contexts to enable
natural conditional checks like ``if not is_absent(value)``. Python provides
two approaches for creating falsey custom objects:

1. Implement ``__bool__`` to return ``False``
2. Inherit from a base class that provides this behavior

The ``falsifier`` package provides a ``Falsifier`` base class specifically
designed for objects that should always evaluate to ``False``. This package is
maintained by the same author and follows the same design philosophy.

The key requirement is that absence sentinels should be falsey without requiring
each sentinel class to implement the behavior independently.

Decision
===============================================================================

Inherit from ``falsifier.Falsifier`` as the base class for ``AbsenceFactory``
rather than implementing ``__bool__`` directly.

Alternatives
===============================================================================

**Implement __bool__ directly in AbsenceFactory**

Rejected because:

- Duplicates functionality available in a focused, reusable library
- Violates DRY principle when a well-tested implementation exists
- Increases maintenance burden by duplicating logic across packages
- Misses opportunity to leverage specialized package for common pattern

**Use composition with a falsey mixin**

Rejected because:

- Adds unnecessary complexity for single-behavior inheritance
- Inheritance hierarchy is already simple and focused
- No compelling reason to prefer composition over inheritance here
- Would require additional boilerplate for the same result

**Do nothing (leave sentinels truthy)**

Rejected because:

- Contradicts the primary use case of representing absence
- Creates confusing semantics where "absent" evaluates to True
- Forces users to always use explicit ``is_absent()`` checks
- Inconsistent with Python conventions for sentinel values

Consequences
===============================================================================

**Positive:**

- Leverages well-tested, focused library for falsey behavior
- Maintains consistency with other packages in the project family
- Reduces code duplication across related packages
- Clear separation between absence semantics and falsey implementation
- Enables focus on absence-specific features rather than basic behavior

**Negative:**

- Adds external dependency on ``falsifier`` package
- Introduces small coupling between packages
- Users must install ``falsifier`` as a dependency
- Changes to ``falsifier`` API could require updates

**Neutral:**

- Establishes pattern for reusing behavior across package family
- Reinforces focus on single-purpose, composable packages
