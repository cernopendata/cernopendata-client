# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file verifier tests."""

import os
import subprocess

from click.testing import CliRunner
from cernopendata_client.cli import download_files, verify_files
from cernopendata_client.verifier import (
    get_file_size,
    get_file_checksum,
    get_file_info_local,
)


def test_get_file_size():
    """Test get_file_size()."""
    afile = "./LICENSE"
    assert get_file_size(afile) == 35149


def test_get_file_checksum():
    """Test get_file_checksum()."""
    afile = "./LICENSE"
    assert get_file_checksum(afile) == "adler32:f70779ec"


def test_get_file_info_local_wrong_input():
    """Test get_file_info_local() for wrong inputs."""

    assert get_file_info_local(123456) == []


def test_get_file_info_local_good_input():
    """Test get_file_info_local() for good inputs."""

    # remove test file
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)

    # first download it
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # now test get_file_info_local()
    test_result = get_file_info_local(3005)
    assert len(test_result) == 1
    assert test_result[0]["name"] == "0d0714743f0204ed3c0144941e6ce248.configFile.py"
    assert test_result[0]["size"] == 3644
    assert test_result[0]["checksum"] == "adler32:be83a186"

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert test_result.output.endswith("\n==> Success!\n")

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_get_file_info_local_good_input_wrong_count():
    """Test get_file_info_local() for good inputs simulating wring file count."""

    # remove test file
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)

    # first download it
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # simulate getting more files
    cmd = "cp {} {}.extra".format(test_file, test_file)
    subprocess.check_output(cmd, shell=True)

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1

    # remove test files
    if os.path.isfile(test_file + ".extra"):
        os.remove(test_file + ".extra")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_get_file_info_local_good_input_wrong_checksum():
    """Test get_file_info_local() for good inputs simulating wrong file checksum."""

    # remove test file
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)

    # first download it
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # simulate checksum change
    cmd = "sed -i -e 's,a,b,g' {}".format(test_file)
    subprocess.check_output(cmd, shell=True)

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_get_file_info_local_good_input_wrong_size():
    """Test get_file_info_local() for good inputs simulating wrong file size."""

    # remove test file
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)

    # first download it
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")

    # simulate checksum change
    cmd = "sed -i -e 's,a,bbbbbb,g' {}".format(test_file)
    subprocess.check_output(cmd, shell=True)

    # now test verifier
    test_verifier_files = CliRunner()
    test_result = test_verifier_files.invoke(verify_files, ["--recid", 3005])
    assert test_result.exit_code == 1

    # remove test file
    if os.path.isfile(test_file):
        os.remove(test_file)
