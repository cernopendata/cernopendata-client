# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.
"""cernopendata-client version test."""

from cernopendata_client import __version__
from click.testing import CliRunner
from cernopendata_client.cli import version


def test_version():
    """Test version import."""
    test_version = CliRunner()
    test_result = test_version.invoke(version)
    assert test_result.exit_code == 0
    assert test_result.output == __version__ + "\n"
