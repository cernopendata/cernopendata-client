# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command download-files test."""

import os
import pytest

from click.testing import CliRunner
from cernopendata_client.cli import download_files
from cernopendata_client.config import SERVER_HTTPS_URI


def test_dry_run_from_recid():
    """Test `download-files --recid --dry-run` command."""
    test_dry_run = CliRunner()
    test_result = test_dry_run.invoke(download_files, ["--recid", 3005, "--dry-run"])
    assert test_result.exit_code == 0
    assert "0d0714743f0204ed3c0144941e6ce248.configFile.py" in test_result.output


def test_dry_run_from_recid_wrong():
    """Test `download-files --recid --dry-run` command for wrong values."""
    test_dry_run = CliRunner()
    test_result = test_dry_run.invoke(download_files, ["--recid", 0])
    assert test_result.exit_code == 2


def test_dry_run_from_doi():
    """Test `download-files --doi --dry-run` command."""
    test_dry_run = CliRunner()
    test_result = test_dry_run.invoke(
        download_files,
        ["--doi", "10.7483/OPENDATA.CMS.A342.9982", "--no-expand", "--dry-run"],
    )
    assert test_result.exit_code == 0
    assert (
        "CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0001_file_index.json"
        in test_result.output
    )


def test_dry_run_from_doi_wrong():
    """Test `download-files --doi --dry-run` command for wrong values."""
    test_dry_run = CliRunner()
    test_result = test_dry_run.invoke(
        download_files, ["--doi", "NONEXISTING", "--no-expand", "--dry-run"]
    )
    assert test_result.exit_code == 2


def test_download_files_http_pycurl():
    """Test download_files() command with http protocol using pycurl."""
    pycurl = pytest.importorskip("pycurl")  # noqa: F841
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_http_requests(mocker):
    """Test download_files() command with http protocol using requests."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_https_pycurl():
    """Test download_files() command with https protocol using pycurl."""
    pycurl = pytest.importorskip("pycurl")  # noqa: F841
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_https_requests(mocker):
    """Test download_files() command with https protocol using requests."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_download_engine(mocker):
    """Test download_files() command with download-engine option."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--download-engine", "requests"]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_download_engine_wrong_protocol_combination_one():
    """Test download_files() command with download-engine option and wrong protocol."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files,
        ["--recid", 3005, "--download-engine", "requests", "--protocol", "xrootd"],
    )
    assert test_result.exit_code == 1
    assert "requests is not compatible with xrootd" in test_result.output


def test_download_files_download_engine_wrong_protocol_combination_two():
    """Test download_files() command with download-engine option and wrong protocol."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files,
        ["--recid", 3005, "--download-engine", "xrootd", "--protocol", "http"],
    )
    assert test_result.exit_code == 1
    assert "xrootd is not compatible with http" in test_result.output


def test_download_files_root():
    """Test download_files() command with xrootd protocol."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--protocol", "xrootd"]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_root_wrong(mocker):
    """Test download_files() command with xrootd protocol without xrootd."""
    mocker.patch("cernopendata_client.downloader.xrootd_available", False)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--protocol", "xrootd"]
    )
    assert test_result.exit_code == 1
    assert "xrootd is not installed on system" in test_result.output


def test_download_files_with_verify():
    """Test download_files() --verify command."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files = CliRunner()
    test_result = test_download_files.invoke(
        download_files, ["--recid", 3005, "--verify"]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_empty_value():
    """Test download_files() command with empty value."""
    test_download_files_empty_value = CliRunner()
    test_result = test_download_files_empty_value.invoke(download_files)
    assert test_result.exit_code == 1
    assert "Please provide at least one of following arguments" in test_result.output


def test_download_files_wrong_value():
    """Test download_files() command with wrong value."""
    test_download_files_empty_value = CliRunner()
    test_result = test_download_files_empty_value.invoke(
        download_files,
        ["--recid", 5500, "--server", "foo"],
    )
    assert test_result.exit_code == 2
    assert "Invalid value for --server" in test_result.output


def test_download_files_filter_name():
    """Test download_files() command with --filter-name <name>."""
    test_file = "5500/BuildFile.xml"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files_filter = CliRunner()
    test_result_name = test_download_files_filter.invoke(
        download_files,
        [
            "--recid",
            5500,
            "--filter-name",
            "BuildFile.xml",
        ],
    )
    assert test_result_name.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert test_result_name.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)


def test_download_files_filter_name_multiple_values():
    """Test download_files() command with --filter-name <name1>,<name2>."""
    test_files = ["5500/BuildFile.xml", "5500/List_indexfile.txt"]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_name = test_download_files_filter.invoke(
        download_files,
        [
            "--recid",
            5500,
            "--filter-name",
            "BuildFile.xml,List_indexfile.txt",
        ],
    )
    assert test_result_name.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_name.output.endswith("\n==> Success!\n")


def test_download_files_filter_name_wrong():
    """Test download_files() command with --filter-name <name> containing wrong value."""
    test_download_files_filter = CliRunner()
    test_result_name = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-name", "test_name.py"]
    )
    assert test_result_name.exit_code == 1
    assert "No files matching the filters" in test_result_name.output


def test_download_files_filter_regexp_single_file():
    """Test download_files() command with --filter-regexp."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    if os.path.isfile(test_file):
        os.remove(test_file)
    test_download_files_filter = CliRunner()
    test_result_regexp = test_download_files_filter.invoke(
        download_files, ["--recid", 3005, "--filter-regexp", "py$"]
    )
    assert test_result_regexp.exit_code == 0
    assert test_result_regexp.output.endswith("\n==> Success!\n")
    if os.path.isfile(test_file):
        os.remove(test_file)
    else:
        pytest.fail("{} not downloaded".format(test_file))


def test_download_files_filter_regexp_multiple_files():
    """Test download_files() command with --filter-regexp."""
    test_files = [
        "5500/HiggsDemoAnalyzer.cc",
        "5500/M4Lnormdatall.cc",
        "5500/M4Lnormdatall_lvl3.cc",
    ]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_regexp = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-regexp", ".cc$"]
    )
    assert test_result_regexp.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_regexp.output.endswith("\n==> Success!\n")


def test_download_files_filter_regexp_wrong():
    """Test download_files() command with --filter-regexp containing wrong value."""
    test_download_files_filter = CliRunner()
    test_result_regexp_three = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-regexp", "wontmatchanything"]
    )
    assert test_result_regexp_three.exit_code == 1
    assert "No files matching the filters" in test_result_regexp_three.output


def test_download_files_filter_range():
    """Test download_files() command with --filter-range <range>."""
    test_files = [
        "5500/BuildFile.xml",
        "5500/HiggsDemoAnalyzer.cc",
        "5500/List_indexfile.txt",
        "5500/M4Lnormdatall.cc",
    ]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_range = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-range", "1-4"]
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_range.output.endswith("\n==> Success!\n")


def test_download_files_filter_range_multiple_values():
    """Test download_files() command with --filter-range <range1>,<range2>."""
    test_files = [
        "5500/BuildFile.xml",
        "5500/HiggsDemoAnalyzer.cc",
        "5500/M4Lnormdatall_lvl3.cc",
        "5500/demoanalyzer_cfg_level3MC.py",
        "5500/demoanalyzer_cfg_level3data.py",
    ]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_range = test_download_files_filter.invoke(
        download_files, ["--recid", 5500, "--filter-range", "1-2,5-7"]
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_range.output.endswith("\n==> Success!\n")


def test_download_files_filter_single_range_single_regexp():
    """Test download_files() command with --filter-regexp <regexp> --filter-range <range>."""
    test_files = [
        "5500/demoanalyzer_cfg_level3MC.py",
        "5500/demoanalyzer_cfg_level3data.py",
    ]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_range = test_download_files_filter.invoke(
        download_files,
        ["--recid", 5500, "--filter-regexp", "py", "--filter-range", "1-2"],
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_range.output.endswith("\n==> Success!\n")


def test_download_files_filter_multiple_range_single_regexp():
    """Test download_files() command with --filter-regexp <regexp> --filter-range <range1>,<range2>."""
    test_files = [
        "5500/demoanalyzer_cfg_level3MC.py",
        "5500/demoanalyzer_cfg_level3data.py",
        "5500/demoanalyzer_cfg_level4data.py",
    ]
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
    test_download_files_filter = CliRunner()
    test_result_range = test_download_files_filter.invoke(
        download_files,
        [
            "--recid",
            5500,
            "--filter-regexp",
            "py",
            "--filter-range",
            "1-2,4-4",
        ],
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        if os.path.isfile(file_location):
            os.remove(file_location)
        else:
            pytest.fail("{} not downloaded".format(file_location))
    assert test_result_range.output.endswith("\n==> Success!\n")
