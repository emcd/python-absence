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
002. Non-Picklable Sentinels
*******************************************************************************

Status
===============================================================================

Accepted

Context
===============================================================================

Absence sentinels rely on identity checks (``is`` operator) for correctness.
The ``is_absent()`` predicate uses ``absent is value`` to determine if a value
is the global absence sentinel. Singleton semantics are critical for this
identity-based checking to work reliably.

Python's ``pickle`` module serializes objects for storage or transmission and
recreates them during unpickling. By default, unpickling creates new object
instances, which breaks singleton semantics:

- ``pickle.loads(pickle.dumps(absent)) is absent`` would be ``False``
- Multiple "copies" of sentinels would exist after unpickling
- Identity-based checks would fail unpredictably

While custom ``__reduce__`` implementations can preserve singleton semantics
during unpickling, this requires careful coordination and increases complexity.

The fundamental question is whether absence sentinels should be serializable at
all, and if so, what guarantees should be provided.

Decision
===============================================================================

Make absence sentinels explicitly non-picklable by implementing ``__reduce__``
to raise ``OperationValidityError``.

Alternatives
===============================================================================

**Implement singleton-preserving pickle support**

Rejected because:

- Absence sentinels represent transient "missing value" states in function calls
- Serializing absence sentinels indicates likely design smell in calling code
- Complexity of singleton preservation during unpickling outweighs benefits
- Better to fail explicitly than create subtle identity bugs
- Forces users to handle absence before serialization boundary

**Allow default pickling behavior**

Rejected because:

- Breaks singleton semantics silently after unpickling
- Creates subtle bugs where ``is`` checks fail unexpectedly
- Users might not realize unpickling creates distinct instances
- Violates principle of least surprise for sentinel objects

**Do nothing (inherit pickle behavior from base class)**

Rejected because:

- Unclear what ``falsifier.Falsifier`` pickle behavior is
- Leaves critical semantic guarantee to inherited implementation
- Should explicitly document this architectural constraint
- Making picklability explicit improves API clarity

Consequences
===============================================================================

**Positive:**

- Prevents subtle identity-based bugs from pickle/unpickle cycles
- Forces explicit handling of absence before serialization boundaries
- Clear error message when attempting invalid operation
- Maintains singleton semantic guarantees across all code paths
- Encourages better API design (resolve absence before serialization)

**Negative:**

- Cannot serialize data structures containing absence sentinels
- Users must explicitly handle absence before pickling
- Adds restriction that some users might find inconvenient
- Requires wrapping or transformation before serialization

**Neutral:**

- Aligns with common sentinel object patterns in Python ecosystem
- Consistent with ``Ellipsis`` and other singleton semantics
- Encourages treating absence as transient intermediate state
