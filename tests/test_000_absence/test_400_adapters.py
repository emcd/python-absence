# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#


''' Assert correct function of dataclass adaptation helpers. '''


from dataclasses import dataclass, field
from typing import ClassVar

import pytest

from absence.adapters import adapt_dataclass
from absence.exceptions import OperationValidityError
from absence.objects import Absential, absent, is_present


# 100: Basic extraction

@dataclass
class _Simple:
    name: str | None = None
    value: int | None = None


def test_100_extracts_all_present_fields( ):
    ''' Fields with non-None values appear in result. '''
    obj = _Simple( name = 'Alice', value = 42 )
    result = adapt_dataclass( obj )
    assert result == { 'name': 'Alice', 'value': 42 }


def test_101_skips_none_by_default( ):
    ''' Fields with None value omitted when skip_value is default. '''
    obj = _Simple( name = 'Alice' )
    result = adapt_dataclass( obj )
    assert result == { 'name': 'Alice' }


def test_102_all_none_produces_empty_dict( ):
    ''' All-None dataclass yields empty dict. '''
    obj = _Simple( )
    result = adapt_dataclass( obj )
    assert result == { }


def test_103_preserves_none_as_value( ):
    ''' None stored as a real value when skip_value differs. '''
    obj = _Simple( name = None, value = 42 )
    sentinel = object( )
    result = adapt_dataclass( obj, skip_value = sentinel )
    assert result == { 'name': None, 'value': 42 }


# 200: Custom skip values

_UNSET = object( )


@dataclass
class _WithSentinel:
    name: str | object = _UNSET
    email: str | object = _UNSET


def test_200_custom_skip_value( ):
    ''' Custom sentinel fields skipped when provided as skip_value. '''
    obj = _WithSentinel( name = 'Bob' )
    result = adapt_dataclass( obj, skip_value = _UNSET )
    assert result == { 'name': 'Bob' }


def test_201_none_not_skipped_with_custom_sentinel( ):
    ''' None preserved when skip_value is a different sentinel. '''
    obj = _WithSentinel( name = None, email = 'bob@example.com' )
    result = adapt_dataclass( obj, skip_value = _UNSET )
    assert result == { 'name': None, 'email': 'bob@example.com' }


# 300: Error cases

def test_300_non_dataclass_raises( ):
    ''' Non-dataclass objects raise OperationValidityError. '''
    with pytest.raises( OperationValidityError ):
        adapt_dataclass( 42 )


def test_301_plain_object_raises( ):
    ''' Plain object instances raise OperationValidityError. '''
    with pytest.raises( OperationValidityError ):
        adapt_dataclass( object( ) )


def test_302_dataclass_class_raises( ):
    ''' Dataclass type (not instance) raises OperationValidityError. '''
    with pytest.raises( OperationValidityError ):
        adapt_dataclass( _Simple )


def test_303_list_raises( ):
    ''' Built-in collections raise OperationValidityError. '''
    with pytest.raises( OperationValidityError ):
        adapt_dataclass( [ 1, 2, 3 ] )


# 400: Field inclusion semantics

@dataclass
class _Parent:
    name: str | None = None


@dataclass
class _Child( _Parent ):
    email: str | None = None


def test_400_inherited_fields_included( ):
    ''' Fields from parent dataclass appear in result. '''
    obj = _Child( name = 'Carol', email = 'carol@example.com' )
    result = adapt_dataclass( obj )
    assert result == { 'name': 'Carol', 'email': 'carol@example.com' }


@dataclass
class _WithClassVar:
    name: str | None = None
    registry: ClassVar[ list[ str ] ] = [ ]


def test_401_classvar_excluded( ):
    ''' ClassVar-annotated fields do not appear in result. '''
    obj = _WithClassVar( name = 'Dave' )
    result = adapt_dataclass( obj )
    assert 'registry' not in result
    assert result == { 'name': 'Dave' }


@dataclass
class _WithInitFalse:
    name: str | None = None
    cached: str = field( default = 'default', init = False )


def test_402_init_false_field_included( ):
    ''' Fields with init=False still appear in result. '''
    obj = _WithInitFalse( name = 'Eve' )
    result = adapt_dataclass( obj )
    assert result == { 'name': 'Eve', 'cached': 'default' }


# 500: Integration with Absential functions


def _update_user(
    name: Absential[ str ] = absent,
    email: Absential[ str ] = absent,
) -> dict[ str, object ]:
    result: dict[ str, object ] = { }
    if is_present( name ):
        result[ 'name' ] = name
    if is_present( email ):
        result[ 'email' ] = email
    return result


@dataclass
class _UpdateCommand:
    name: str | None = None
    email: str | None = None


def test_500_bridges_cli_to_absential( ):
    ''' adapt_dataclass enables CLI dataclass to Absential kwargs. '''
    cmd = _UpdateCommand( name = 'Frank' )
    kwargs = adapt_dataclass( cmd )
    result = _update_user( **kwargs )
    assert result == { 'name': 'Frank' }


def test_501_empty_command_yields_absent_defaults( ):
    ''' All-skipped fields trigger absent defaults in target function. '''
    cmd = _UpdateCommand( )
    kwargs = adapt_dataclass( cmd )
    result = _update_user( **kwargs )
    assert result == { }
