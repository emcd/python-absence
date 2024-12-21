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


Objects
===============================================================================

The ``absence`` package provides the ``absent`` sentinel and ``AbsenceFactory``
class for representing absent values in contexts where ``None`` might be a
valid value.

Basic Usage
-------------------------------------------------------------------------------

The ``absent`` sentinel can be used directly to represent missing values:

.. doctest:: Absence

    >>> from absence import absent, is_absent
    >>> bool( absent )  # Always evaluates to False
    False
    >>> str( absent )   # Simple string form
    'absent'
    >>> repr( absent )  # Detailed representation
    'absence.absent'
    >>> is_absent( absent )  # Type-safe checking
    True
    >>> is_absent( None )
    False


Type Alias and Predicate Function
-------------------------------------------------------------------------------

The ``absent`` sentinel can help build dynamic SQL queries by distinguishing
between "don't include this field in the query" (``absent``) and "explicitly
query for NULL" (``None``):

.. doctest:: Absence

    >>> from absence import absent, is_absent, Absential
    >>> def build_query(
    ...     name: Absential[ str | None ] = absent,
    ...     email: Absential[ str | None ] = absent,
    ... ) -> str:
    ...     ''' Builds SQL query with optional name and email filters.
    ...
    ...         Absent value means "don't filter on this field".
    ...         None value means "filter for NULL".
    ...         String value means "filter for exact match".
    ...     '''
    ...     conditions = [ ]
    ...     params = [ ]
    ...     if not is_absent( name ):
    ...         if name is None: conditions.append( 'name IS NULL' )
    ...         else:
    ...             conditions.append( 'name = ?' )
    ...             params.append( name )
    ...     if not is_absent( email ):
    ...         if email is None: conditions.append( 'email IS NULL' )
    ...         else:
    ...             conditions.append( 'email = ?' )
    ...             params.append( email )
    ...     query = 'SELECT * FROM users'
    ...     if conditions:
    ...         query += ' WHERE ' + ' AND '.join( conditions )
    ...     return f'Query: {query}, Params: {params}'
    >>> # No filters
    >>> build_query( )
    'Query: SELECT * FROM users, Params: []'
    >>> # Filter for NULL name only
    >>> build_query( name = None )
    'Query: SELECT * FROM users WHERE name IS NULL, Params: []'
    >>> # Filter for specific name and NULL email
    >>> build_query( name = 'Alice', email = None )
    "Query: SELECT * FROM users WHERE name = ? AND email IS NULL, Params: ['Alice']"
    >>> # Filter for specific email only
    >>> build_query( email = 'alice@example.com' )
    "Query: SELECT * FROM users WHERE email = ?, Params: ['alice@example.com']"

.. warning::
   This example demonstrates query building concepts only. In production code,
   always use your database library's parameterized query support to prevent
   SQL injection vulnerabilities.


Custom Absence Types
-------------------------------------------------------------------------------

The ``AbsenceFactory`` allows creation of package-specific absence sentinels:

.. doctest:: Absence

    >>> from absence import AbsenceFactory
    >>> class ConfigValue:
    ...     ''' Configuration value with optional default. '''
    ...     UNSET = AbsenceFactory(
    ...         repr_function = lambda self: 'ConfigValue.UNSET',
    ...         str_function = lambda self: '<unset>' )
    ...
    ...     def __init__( self, value = UNSET ):
    ...         self.value = value
    ...
    ...     def __str__( self ) -> str:
    ...         if self.value is self.UNSET:
    ...             return '<ConfigValue: unset>'
    ...         return f'<ConfigValue: {self.value}>'
    >>> config = ConfigValue( )
    >>> str( config )
    '<ConfigValue: unset>'
    >>> bool( config.value )  # UNSET is falsey
    False
    >>> str( config.value )   # Custom string representation
    '<unset>'
    >>> repr( config.value )  # Custom repr
    'ConfigValue.UNSET'


Builtins Integration
-------------------------------------------------------------------------------

The ``absent`` sentinel and ``is_absent`` predicate can be installed as
builtins:

.. doctest:: Absence

    >>> from absence import install
    >>> install( )  # Default names: 'Absent' and 'isabsent'
    >>> isabsent( Absent )
    True
    >>> # Custom names can be used
    >>> install( sentinel_name = 'MISSING', predicate_name = 'is_missing' )
    >>> is_missing( MISSING )
    True
    >>> # Selective installation
    >>> install( sentinel_name = None, predicate_name = 'check_absent' )
    >>> check_absent( absent )
    True
