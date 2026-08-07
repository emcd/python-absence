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


''' Assert correct function of AbsenceCell container. '''


import pytest

from absence.cell import AbsenceCell
from absence.exceptions import CellStateError


# 100: Construction

def test_100_empty_cell_creation( ):
    ''' Default constructor produces cell containing absent. '''
    cell = AbsenceCell( )
    assert cell.is_absent( )


def test_101_occupied_cell_creation( ):
    ''' Value constructor produces cell containing that value. '''
    cell = AbsenceCell( 42 )
    assert cell.is_present( )


def test_102_immutability_slots( ):
    ''' Cell prevents attribute addition via slots. '''
    cell = AbsenceCell( 42 )
    with pytest.raises( AttributeError ):
        cell.extra = 'forbidden'


# 200: Predicates

def test_200_is_absent_on_empty( ):
    ''' Empty cell reports absent. '''
    assert AbsenceCell( ).is_absent( )


def test_201_is_absent_on_occupied( ):
    ''' Occupied cell reports not absent. '''
    assert not AbsenceCell( 42 ).is_absent( )


def test_202_is_present_on_occupied( ):
    ''' Occupied cell reports present. '''
    assert AbsenceCell( 42 ).is_present( )


def test_203_is_present_on_empty( ):
    ''' Empty cell reports not present. '''
    assert not AbsenceCell( ).is_present( )


def test_204_bool_occupied( ):
    ''' Occupied cell evaluates to True. '''
    assert bool( AbsenceCell( 0 ) )
    assert bool( AbsenceCell( None ) )
    assert bool( AbsenceCell( False ) )


def test_205_bool_empty( ):
    ''' Empty cell evaluates to False. '''
    assert not bool( AbsenceCell( ) )


# 300: Extraction

def test_300_extract_occupied( ):
    ''' Extract returns contained value from occupied cell. '''
    assert AbsenceCell( 42 ).extract( ) == 42


def test_301_extract_empty_raises( ):
    ''' Extract from empty cell raises CellStateError. '''
    with pytest.raises( CellStateError ):
        AbsenceCell( ).extract( )


def test_302_extract_or_occupied( ):
    ''' Extract_or returns value from occupied cell. '''
    assert AbsenceCell( 42 ).extract_or( 0 ) == 42


def test_303_extract_or_empty( ):
    ''' Extract_or returns default from empty cell. '''
    assert AbsenceCell( ).extract_or( 99 ) == 99


def test_304_extract_or_compute_occupied( ):
    ''' Extract_or_compute returns value from occupied cell. '''
    assert AbsenceCell( 42 ).extract_or_compute( lambda: 99 ) == 42


def test_305_extract_or_compute_empty( ):
    ''' Extract_or_compute calls factory for empty cell. '''
    assert AbsenceCell( ).extract_or_compute( lambda: 99 ) == 99


# 400: Evaluation

def test_400_evaluate_or_occupied( ):
    ''' Evaluate_or applies func to occupied cell. '''
    assert AbsenceCell( 5 ).evaluate_or( lambda n: n * 2, 0 ) == 10


def test_401_evaluate_or_empty( ):
    ''' Evaluate_or returns default for empty cell. '''
    assert AbsenceCell( ).evaluate_or( lambda n: n * 2, 0 ) == 0


def test_402_evaluate_or_true_occupied( ):
    ''' Evaluate_or_true applies predicate to occupied cell. '''
    assert AbsenceCell( 10 ).evaluate_or_true( lambda n: n > 5 )


def test_403_evaluate_or_true_empty( ):
    ''' Evaluate_or_true returns True for empty cell. '''
    assert AbsenceCell( ).evaluate_or_true( lambda n: n > 5 )


def test_404_evaluate_or_false_occupied( ):
    ''' Evaluate_or_false applies predicate to occupied cell. '''
    assert not AbsenceCell( 3 ).evaluate_or_false( lambda n: n > 5 )


def test_405_evaluate_or_false_empty( ):
    ''' Evaluate_or_false returns False for empty cell. '''
    assert not AbsenceCell( ).evaluate_or_false( lambda n: n > 5 )


# 500: Transformation

def test_500_transform_occupied( ):
    ''' Transform applies func and returns new occupied cell. '''
    result = AbsenceCell( 5 ).transform( lambda n: n * 2 )
    assert result.is_present( )
    assert result.extract( ) == 10


def test_501_transform_empty( ):
    ''' Transform on empty cell returns empty cell. '''
    result = AbsenceCell( ).transform( lambda n: n * 2 )
    assert result.is_absent( )


# 600: Chaining

def test_600_or_else_occupied( ):
    ''' Or_else returns original cell when occupied. '''
    original = AbsenceCell( 42 )
    fallback = AbsenceCell( 99 )
    assert original.or_else( fallback ) is original


def test_601_or_else_empty( ):
    ''' Or_else returns alternative when empty. '''
    empty = AbsenceCell( )
    fallback = AbsenceCell( 99 )
    result = empty.or_else( fallback )
    assert result is fallback


# 700: Conversion

def test_700_to_optional_occupied( ):
    ''' To_optional returns value from occupied cell. '''
    assert AbsenceCell( 42 ).to_optional( ) == 42


def test_701_to_optional_empty( ):
    ''' To_optional returns None from empty cell. '''
    assert AbsenceCell( ).to_optional( ) is None


def test_702_to_optional_preserving_none( ):
    ''' To_optional returns None from cell containing None. '''
    assert AbsenceCell( None ).to_optional( ) is None


# 800: Optional Bridge

def test_800_from_optional_none( ):
    ''' From_optional(None) produces empty cell by default. '''
    assert AbsenceCell.from_optional( None ).is_absent( )


def test_801_from_optional_value( ):
    ''' From_optional(value) produces occupied cell. '''
    assert AbsenceCell.from_optional( 42 ).extract( ) == 42


def test_802_from_optional_preserve_none( ):
    ''' From_optional(None, none_is_absent=False) preserves None. '''
    cell = AbsenceCell.from_optional( None, none_is_absent = False )
    assert cell.is_present( )
    assert cell.extract( ) is None


# 900: Equality, Hashing, Representation

def test_900_equality_occupied_same( ):
    ''' Two occupied cells with equal values are equal. '''
    assert AbsenceCell( 42 ) == AbsenceCell( 42 )


def test_901_equality_occupied_different( ):
    ''' Two occupied cells with different values are not equal. '''
    assert AbsenceCell( 42 ) != AbsenceCell( 99 )


def test_902_equality_empty_same( ):
    ''' Two empty cells are equal. '''
    assert AbsenceCell( ) == AbsenceCell( )


def test_903_equality_empty_occupied( ):
    ''' Empty cell is not equal to occupied cell. '''
    assert AbsenceCell( ) != AbsenceCell( 42 )


def test_904_hash_consistency( ):
    ''' Equal cells produce equal hashes. '''
    assert hash( AbsenceCell( 42 ) ) == hash( AbsenceCell( 42 ) )


def test_905_hash_in_set( ):
    ''' Cells are usable in sets. '''
    assert AbsenceCell( 42 ) in { AbsenceCell( 42 ) }


def test_906_repr_occupied( ):
    ''' Repr of occupied cell shows contained value. '''
    assert repr( AbsenceCell( 42 ) ) == 'AbsenceCell( 42 )'


def test_907_repr_empty( ):
    ''' Repr of empty cell shows no value. '''
    assert repr( AbsenceCell( ) ) == 'AbsenceCell( )'


def test_908_str_delegates( ):
    ''' Str delegates to contained value. '''
    assert str( AbsenceCell( 'hello' ) ) == 'hello'


def test_909_str_empty( ):
    ''' Str of empty cell returns absent. '''
    assert str( AbsenceCell( ) ) == 'absent'
