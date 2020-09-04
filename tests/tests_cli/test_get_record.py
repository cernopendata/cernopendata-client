# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command get-record test."""

from click.testing import CliRunner
from cernopendata_client.cli import get_record


def test_get_record():
    """Test get-record command."""
    test_get_record = CliRunner()
    test_result = test_get_record.invoke(get_record, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert type(test_result.output) == str
    assert (
        '"title": "Configuration file for LHE step HIG-Summer11pLHE-00114_1_cfg.py"'
        in test_result.output
    )
