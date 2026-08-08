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


''' Helpers for adapting dataclass instances to Absential parameters.'''


from . import __
from .exceptions import OperationValidityError as _OperationValidityError


def adapt_dataclass(
    obj: __.typx.Annotated[
        object,
        __.ddoc.Doc( ''' Dataclass instance to adapt. ''' ),
    ],
    *,
    skip_value: __.typx.Annotated[
        object,
        __.ddoc.Doc( ''' Field value to omit from result. ''' ),
    ] = None,
) -> dict[ str, __.typx.Any ]:
    ''' Extracts fields from a dataclass instance, skipping sentinel values.

        Useful for bridging CLI dataclasses (which use None for "not
        provided") to functions with Absential parameters (which default
        to absent). Fields whose value matches skip_value by identity are
        omitted, allowing function defaults to apply.
    '''
    if not __.dcls.is_dataclass( obj ) or isinstance( obj, type ):
        raise _OperationValidityError( 'adapt_dataclass' )
    return {
        field.name: getattr( obj, field.name )
        for field in __.dcls.fields( obj )
        if getattr( obj, field.name ) is not skip_value
    }
