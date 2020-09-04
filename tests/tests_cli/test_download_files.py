# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command download-files test."""

import os
from click.testing import CliRunner
from cernopendata_client.cli import download_files


def test_download_files():
    """Test download_files() command."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\nDownload completed!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)
