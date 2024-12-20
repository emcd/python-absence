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


''' Assert correct function of absence objects. '''


import pickle

import pytest

from . import PACKAGE_NAME, cache_import_module


def test_100_singleton_identity( ):
    ''' Global sentinel maintains identity. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    assert module.absent is module.AbsentSingleton( )
    assert module.absent is module.absent


def test_101_singleton_boolean_evaluation( ):
    ''' Global sentinel evaluates to False. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    assert not module.absent
    assert False == bool( module.absent )  # noqa: E712


def test_102_singleton_string_representations( ):
    ''' Global sentinel has expected string representations. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    assert 'absent' == str( module.absent )
    assert 'absence.absent' == repr( module.absent )


def test_200_factory_instantiation( ):
    ''' Factory produces unique instances. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    obj1 = module.AbsenceFactory( )
    obj2 = module.AbsenceFactory( )
    assert obj1 is not obj2
    assert obj1 != obj2


def test_201_factory_boolean_evaluation( ):
    ''' Factory instances evaluate to False. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    obj = module.AbsenceFactory( )
    assert not obj
    assert False == bool( obj )  # noqa: E712


def test_202_factory_default_strings( ):
    ''' Factory instances have expected default string representations. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    obj = module.AbsenceFactory( )
    assert 'absence' == str( obj )
    assert 'absence.AbsenceFactory( )' == repr( obj )


def test_203_factory_custom_strings( ):
    ''' Factory instances support custom string representations. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    obj = module.AbsenceFactory(
        repr_function = lambda self: 'custom_repr',
        str_function = lambda self: 'custom_str',
    )
    assert 'custom_str' == str( obj )
    assert 'custom_repr' == repr( obj )


def test_204_factory_pickle( ):
    ''' Factory instances cannot be pickled. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    exceptions = cache_import_module( f"{PACKAGE_NAME}.exceptions" )
    obj = module.AbsenceFactory( )
    with pytest.raises( exceptions.OperationValidityError ):
        pickle.dumps( obj )


def test_300_is_absent_predicate( ):
    ''' is_absent predicate identifies global sentinel. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    assert module.is_absent( module.absent )
    assert not module.is_absent( module.AbsenceFactory( ) )
    assert not module.is_absent( None )
    assert not module.is_absent( False )


def test_301_is_absence_predicate( ):
    ''' is_absence predicate identifies all absence types. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    assert module.is_absence( module.absent )
    assert module.is_absence( module.AbsenceFactory( ) )
    assert not module.is_absence( None )
    assert not module.is_absence( False )


def test_900_docstring_sanity( ):
    ''' Classes have valid docstrings. '''
    module = cache_import_module( f"{PACKAGE_NAME}.objects" )
    for class_ in ( module.AbsentSingleton, module.AbsenceFactory ):
        assert hasattr( class_, '__doc__' )
        assert isinstance( class_.__doc__, str )
        assert class_.__doc__
