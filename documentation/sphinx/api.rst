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

:tocdepth: 4


*******************************************************************************
API
*******************************************************************************


Package ``absence``
===============================================================================

A sentinel for absent values, distinct from ``None``, with support for creating
package-specific absence sentinels. Particularly useful in contexts where
``None`` is a valid value but you need to detect the absence of a value.

* ``absent``: Global sentinel representing absence, with falsey behavior and
  identity-based equality.

* ``AbsenceFactory``: Creates package-specific absence sentinels with
  customizable string representations.

* ``Absential``: Type alias for values that may be absent, supporting clear
  type hints.

* ``is_absent``: Type-safe predicate for checking if a value is the global
  absence sentinel.

* ``is_absence``: Type-safe predicate for checking if a value is any absence
  sentinel.

* ``install``: Optional function to install absence sentinel and predicates as
  builtins.


Module ``absence.objects``
-------------------------------------------------------------------------------

.. automodule:: absence.objects


Module ``absence.installers``
-------------------------------------------------------------------------------

.. automodule:: absence.installers


Module ``absence.exceptions``
-------------------------------------------------------------------------------

.. automodule:: absence.exceptions
