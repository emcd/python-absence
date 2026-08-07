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

from absence.exceptions import OperationValidityError
from absence.objects import (
    AbsenceFactory,
    AbsentSingleton,
    absent,
    is_absence,
    is_absent,
)


def test_100_singleton_identity( ):
    ''' Global sentinel maintains identity across reinstantiation. '''
    assert absent is AbsentSingleton( )


def test_101_singleton_boolean_evaluation( ):
    ''' Global sentinel evaluates to False. '''
    assert not absent
    assert False is bool( absent )


def test_102_singleton_string_representations( ):
    ''' Global sentinel has fixed string representations. '''
    assert 'absent' == str( absent )
    assert 'absence.absent' == repr( absent )


def test_103_singleton_pickle_rejection( ):
    ''' Global singleton cannot be pickled. '''
    with pytest.raises( OperationValidityError ):
        pickle.dumps( absent )


def test_200_factory_instantiation( ):
    ''' Factory produces unique instances. '''
    obj1 = AbsenceFactory( )
    obj2 = AbsenceFactory( )
    assert obj1 is not obj2
    assert obj1 != obj2


def test_201_factory_boolean_evaluation( ):
    ''' Factory instances evaluate to False. '''
    obj = AbsenceFactory( )
    assert not obj
    assert False is bool( obj )


def test_202_factory_default_strings( ):
    ''' Factory instances have default string representations. '''
    obj = AbsenceFactory( )
    assert 'absence' == str( obj )
    assert 'absence.AbsenceFactory( )' == repr( obj )


def test_203_factory_custom_strings( ):
    ''' Factory instances support custom string representations. '''
    obj = AbsenceFactory(
        repr_function = lambda self: 'custom_repr',
        str_function = lambda self: 'custom_str',
    )
    assert 'custom_str' == str( obj )
    assert 'custom_repr' == repr( obj )


def test_204_factory_custom_repr_only( ):
    ''' Factory instances support custom repr independently of str. '''
    obj = AbsenceFactory(
        repr_function = lambda self: 'custom_repr',
    )
    assert 'absence' == str( obj )
    assert 'custom_repr' == repr( obj )


def test_205_factory_custom_str_only( ):
    ''' Factory instances support custom str independently of repr. '''
    obj = AbsenceFactory(
        str_function = lambda self: 'custom_str',
    )
    assert 'custom_str' == str( obj )
    assert 'absence.AbsenceFactory( )' == repr( obj )


def test_206_factory_pickle_rejection( ):
    ''' Factory instances cannot be pickled. '''
    obj = AbsenceFactory( )
    with pytest.raises( OperationValidityError ):
        pickle.dumps( obj )


def test_300_global_sentinel_recognition( ):
    ''' Global sentinel is distinguished from lookalikes. '''
    assert is_absent( absent )
    assert not is_absent( AbsenceFactory( ) )
    assert not is_absent( None )
    assert not is_absent( False )


def test_301_absence_type_recognition( ):
    ''' All absence sentinels are recognized as absence type. '''
    assert is_absence( absent )
    assert is_absence( AbsenceFactory( ) )
    assert not is_absence( None )
    assert not is_absence( False )


def test_900_docstring_sanity( ):
    ''' Classes have valid docstrings. '''
    for class_ in ( AbsentSingleton, AbsenceFactory ):
        assert hasattr( class_, '__doc__' )
        assert isinstance( class_.__doc__, str )
        assert class_.__doc__
