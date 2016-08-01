"""Unit tests for core functions, such as those found in data.core."""

import sys

import pytest
import mock

from ...utils import settings

import gips

def t_version_override(mocker):
    """Test Data.meta_dict() for correct override of __version__."""
    settings_fn = mocker.patch.object(gips, 'settings')
    settings_obj = mock.Mock(spec=['EMAIL']) # nothing but EMAIL is available now
    settings_fn.return_value = settings_obj

    gips.version.__version__ = 'orig-version' # no mocking, just overwrite
    version_a = gips.detect_version()

    settings_obj.OVERRIDE_VERSION = 'overridden-version'
    version_b = gips.detect_version()

    assert (version_a, version_b) == ('orig-version', 'overridden-version')
