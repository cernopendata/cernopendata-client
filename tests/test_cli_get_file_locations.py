# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command get-file-locations test."""

from click.testing import CliRunner
from cernopendata_client.cli import get_file_locations


def test_get_file_locations():
    """Test get-file-locations command."""
    test_get_file_locations = CliRunner()
    test_result = test_get_file_locations.invoke(get_file_locations, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert "0d0714743f0204ed3c0144941e6ce248.configFile.py" in test_result.output
