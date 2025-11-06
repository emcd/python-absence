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


''' Assert correct function of builtin installation. '''


import builtins

import pytest

from .__ import PACKAGE_NAME, cache_import_module


@pytest.fixture
def cleanup_builtins( ):
    ''' Remove test attributes from builtins after test. '''
    yield
    for name in ( 'Absent', 'isabsent', 'CustomAbsent', 'custom_absent' ):
        if hasattr( builtins, name ):
            delattr( builtins, name )


def test_100_default_install( cleanup_builtins ):
    ''' Default installation works. '''
    module = cache_import_module( f"{PACKAGE_NAME}.installers" )
    objects = cache_import_module( f"{PACKAGE_NAME}.objects" )
    module.install( )
    assert hasattr( builtins, 'Absent' )
    assert hasattr( builtins, 'isabsent' )
    assert objects.absent is builtins.Absent
    assert objects.is_absent is builtins.isabsent


def test_101_custom_install( cleanup_builtins ):
    ''' Custom installation works. '''
    module = cache_import_module( f"{PACKAGE_NAME}.installers" )
    objects = cache_import_module( f"{PACKAGE_NAME}.objects" )
    module.install(
        sentinel_name = 'CustomAbsent',
        predicate_name = 'custom_absent',
    )
    assert hasattr( builtins, 'CustomAbsent' )
    assert hasattr( builtins, 'custom_absent' )
    assert objects.absent is builtins.CustomAbsent
    assert objects.is_absent is builtins.custom_absent


def test_102_partial_install( cleanup_builtins ):
    ''' Partial installation works. '''
    module = cache_import_module( f"{PACKAGE_NAME}.installers" )
    module.install( sentinel_name = None )
    assert not hasattr( builtins, 'Absent' )
    assert hasattr( builtins, 'isabsent' )
    delattr( builtins, 'isabsent' )
    module.install( predicate_name = None )
    assert hasattr( builtins, 'Absent' )
    assert not hasattr( builtins, 'isabsent' )
