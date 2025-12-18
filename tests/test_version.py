# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.
"""cernopendata-client version test."""

import pytest

from cernopendata_client import __version__
from cernopendata_client.cli import version


@pytest.mark.local
def test_version(cli_runner):
    """Test version import."""
    test_result = cli_runner.invoke(version)
    assert test_result.exit_code == 0
    assert test_result.output == __version__ + "\n"
