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


''' Immutable container wrapping Absential[T] with conditional API. '''


from . import __
from .exceptions import CellStateError as _CellStateError
from .objects import Absential as _Absential
from .objects import absent as _absent
from .objects import is_absent as _is_absent


_T = __.typx.TypeVar( '_T' )
_R = __.typx.TypeVar( '_R' )


class AbsenceCell( __.typx.Generic[ _T ] ):
    ''' Wraps an Absential[T] value with a rich conditional API.

        Provides safe extraction, evaluation, transformation, and chaining
        for values that may be absent, without requiring manual boolean
        checks or repeated is_absent guards.
    '''

    __slots__ = ( '_value', )

    _value: _Absential[ _T ]

    def __init__(
        self,
        value: __.typx.Annotated[
            _Absential[ _T ],
            __.ddoc.Doc( ''' Value to wrap. Defaults to absent. ''' ),
        ] = _absent,
    ) -> None:
        object.__setattr__( self, '_value', value )


    def __setattr__( self, name: str, value: object ) -> None:
        raise AttributeError( 'AbsenceCell is immutable.' )  # noqa: TRY003


    def __delattr__( self, name: str ) -> None:
        raise AttributeError( 'AbsenceCell is immutable.' )  # noqa: TRY003


    def __bool__( self ) -> bool:
        return self._value is not _absent


    def __eq__( self, other: object ) -> bool:
        if not isinstance( other, AbsenceCell ): return NotImplemented
        # isinstance narrows to AbsenceCell but drops the type parameter,
        # so other._value is Absential[Unknown]. The == comparison is
        # correct regardless: absent uses identity, values use __eq__.
        return self._value == other._value  # pyright: ignore


    def __hash__( self ) -> int:
        return hash( self._value )


    def __repr__( self ) -> str:
        if self._value is _absent: return 'AbsenceCell( )'
        return f'AbsenceCell( {self._value!r} )'


    def __str__( self ) -> str:
        if self._value is _absent: return 'absent'
        return str( self._value )


    @classmethod
    def from_optional(
        cls,
        value: __.typx.Annotated[
            _T | None,
            __.ddoc.Doc( ''' Optional value to bridge. ''' ),
        ],
        none_is_absent: __.typx.Annotated[
            bool,
            __.ddoc.Doc(
                ''' Whether None produces empty cell. ''' ),
        ] = True,
    ) -> __.typx.Self:
        ''' Creates cell from Optional[T], bridging None semantics.

            When none_is_absent is True (default), None produces an empty
            cell. When False, None is stored as an occupied value.
        '''
        if none_is_absent and value is None:
            return cls( )
        return cls( value )  # type: ignore[arg-type]


    def evaluate_or(
        self,
        func: __.typx.Annotated[
            __.cabc.Callable[ [ _T ], _R ],
            __.ddoc.Doc( ''' Function applied to contained value. ''' ),
        ],
        default: __.typx.Annotated[
            _R,
            __.ddoc.Doc( ''' Result for empty cells. ''' ),
        ],
    ) -> _R:
        ''' Applies func to value, or returns default if cell is empty. '''
        value = self._value
        if _is_absent( value ): return default
        return func( value )


    def evaluate_or_false(
        self,
        predicate: __.typx.Annotated[
            __.cabc.Callable[ [ _T ], bool ],
            __.ddoc.Doc( ''' Predicate applied to contained value. ''' ),
        ],
    ) -> bool:
        ''' Applies predicate, returning False if cell is empty. '''
        value = self._value
        if _is_absent( value ): return False
        return predicate( value )


    def evaluate_or_true(
        self,
        predicate: __.typx.Annotated[
            __.cabc.Callable[ [ _T ], bool ],
            __.ddoc.Doc( ''' Predicate applied to contained value. ''' ),
        ],
    ) -> bool:
        ''' Applies predicate, returning True if cell is empty. '''
        value = self._value
        if _is_absent( value ): return True
        return predicate( value )


    def extract( self ) -> _T:
        ''' Extracts the contained value.

            Raises CellStateError if cell is empty.
        '''
        value = self._value
        if _is_absent( value ):
            raise _CellStateError( )
        return value


    def extract_or(
        self,
        default: __.typx.Annotated[
            _T,
            __.ddoc.Doc( ''' Fallback for empty cells. ''' ),
        ],
    ) -> _T:
        ''' Extracts value, or returns default if cell is empty. '''
        value = self._value
        if _is_absent( value ): return default
        return value


    def extract_or_compute(
        self,
        factory: __.typx.Annotated[
            __.cabc.Callable[ [ ], _T ],
            __.ddoc.Doc( ''' Factory called for empty cells. ''' ),
        ],
    ) -> _T:
        ''' Extracts value, or returns factory() if cell is empty. '''
        value = self._value
        if _is_absent( value ): return factory( )
        return value


    def is_absent( self ) -> bool:
        ''' Checks if cell contains the absent sentinel. '''
        return self._value is _absent


    def is_present( self ) -> bool:
        ''' Checks if cell contains a present value. '''
        return self._value is not _absent


    def or_else(
        self,
        alternative: __.typx.Annotated[
            'AbsenceCell[ _T ]',
            __.ddoc.Doc( ''' Cell returned if self is empty. ''' ),
        ],
    ) -> 'AbsenceCell[ _T ]':
        ''' Returns self if occupied, or alternative if empty. '''
        if self._value is _absent: return alternative
        return self


    def to_optional( self ) -> __.typx.Optional[ _T ]:
        ''' Returns value if occupied, or None if cell is empty. '''
        value = self._value
        if _is_absent( value ): return None
        return value


    def transform(
        self,
        func: __.typx.Annotated[
            __.cabc.Callable[ [ _T ], _R ],
            __.ddoc.Doc( ''' Function applied to contained value. ''' ),
        ],
    ) -> 'AbsenceCell[ _R ]':
        ''' Returns new cell with func applied, or empty cell. '''
        value = self._value
        if _is_absent( value ): return AbsenceCell( )
        return AbsenceCell( func( value ) )
