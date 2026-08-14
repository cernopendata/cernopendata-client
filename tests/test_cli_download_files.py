# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021, 2025, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command download-files test."""

import os
import zlib

import pytest

from cernopendata_client import verifier
from cernopendata_client.cli import download_files
from cernopendata_client.config import SERVER_HTTPS_URI
from cernopendata_client.searcher import FileEntry


def _checksum(content):
    """Return the metadata checksum for test content."""
    return "adler32:{:08x}".format(zlib.adler32(content, 1) & 0xFFFFFFFF)


def _mock_download_command(mocker, entries, content_by_location):
    """Mock metadata lookup and write requested content like a downloader."""
    record = mocker.patch(
        "cernopendata_client.cli.get_record_as_json",
        return_value={"metadata": {"recid": "42"}},
    )
    file_entries = mocker.patch(
        "cernopendata_client.cli.get_file_entries", return_value=entries
    )

    def write_download(**kwargs):
        content = content_by_location.get(kwargs["file_location"])
        if content is not None:
            destination = os.path.join(
                kwargs["path"], kwargs["file_location"].rsplit("/", 1)[-1]
            )
            with open(destination, "wb") as stream:
                stream.write(content)

    downloader = mocker.patch(
        "cernopendata_client.cli.download_single_file", side_effect=write_download
    )
    return record, file_entries, downloader


@pytest.mark.local
def test_download_files_verifies_checksum_by_default(
    cli_runner, tmp_path, monkeypatch, mocker
):
    """Test same-sized corrupt content cannot report success by default."""
    monkeypatch.chdir(tmp_path)
    location = "http://example.com/data.bin"
    entry = FileEntry(location, 4, _checksum(b"good"))
    record, file_entries, _ = _mock_download_command(
        mocker, [entry], {location: b"evil"}
    )

    result = cli_runner.invoke(download_files, ["--recid", "42"])

    assert result.exit_code == 1
    assert "File checksum does not match" in result.output
    assert "Success!" not in result.output
    record.assert_called_once_with("http://opendata.cern.ch", 42, None, None)
    file_entries.assert_called_once()


@pytest.mark.local
def test_download_files_no_verify_skips_only_checksum(
    cli_runner, tmp_path, monkeypatch, mocker
):
    """Test --no-verify accepts same-sized content without hashing it."""
    monkeypatch.chdir(tmp_path)
    location = "http://example.com/data.bin"
    entry = FileEntry(location, 4, _checksum(b"good"))
    _mock_download_command(mocker, [entry], {location: b"evil"})
    checksum = mocker.spy(verifier, "get_file_checksum")

    result = cli_runner.invoke(download_files, ["--recid", "42", "--no-verify"])

    assert result.exit_code == 0
    assert result.output.endswith("\n==> Success!\n")
    checksum.assert_not_called()


@pytest.mark.local
def test_download_files_no_verify_rejects_truncated_file(
    cli_runner, tmp_path, monkeypatch, mocker
):
    """Test --no-verify retains always-on expected-size validation."""
    monkeypatch.chdir(tmp_path)
    location = "http://example.com/data.bin"
    entry = FileEntry(location, 10, _checksum(b"complete!!"))
    _mock_download_command(mocker, [entry], {location: b"short"})

    result = cli_runner.invoke(download_files, ["--recid", "42", "--no-verify"])

    assert result.exit_code == 1
    assert "Expected size 10, found 5" in result.output
    assert "incomplete" in result.output
    assert "Success!" not in result.output


@pytest.mark.local
def test_download_files_rejects_missing_engine_output(
    cli_runner, tmp_path, monkeypatch, mocker
):
    """Test an engine returning without a destination cannot report success."""
    monkeypatch.chdir(tmp_path)
    location = "http://example.com/data.bin"
    entry = FileEntry(location, 4, _checksum(b"data"))
    _mock_download_command(mocker, [entry], {})

    result = cli_runner.invoke(download_files, ["--recid", "42"])

    assert result.exit_code == 1
    assert "Downloaded file is missing" in result.output
    assert "Success!" not in result.output


@pytest.mark.local
def test_download_files_unexpanded_index_is_explicitly_excluded(
    cli_runner, tmp_path, monkeypatch, mocker
):
    """Test aggregate metadata is not compared to an index JSON response."""
    monkeypatch.chdir(tmp_path)
    location = "http://example.com/record/42/file_index/index.json"
    entry = FileEntry(location, 1000000, "", is_file_index=True)
    _mock_download_command(mocker, [entry], {location: b"{}"})

    result = cli_runner.invoke(download_files, ["--recid", "42", "--no-expand"])

    assert result.exit_code == 0
    assert "Skipping metadata size and checksum checks" in result.output
    assert result.output.index("Verifying file") < result.output.index("Skipping")
    assert result.output.endswith("\n==> Success!\n")


@pytest.mark.local
def test_download_files_help_describes_default_verification(cli_runner):
    """Test CLI help exposes both verification choices and the default."""
    result = cli_runner.invoke(download_files, ["--help"])

    assert result.exit_code == 0
    assert "--verify / --no-verify" in result.output
    assert "default=yes" in result.output


def test_dry_run_from_recid(cli_runner):
    """Test `download-files --recid --dry-run` command."""
    test_result = cli_runner.invoke(download_files, ["--recid", 3005, "--dry-run"])
    assert test_result.exit_code == 0
    assert "0d0714743f0204ed3c0144941e6ce248.configFile.py" in test_result.output


def test_dry_run_from_recid_wrong(cli_runner):
    """Test `download-files --recid --dry-run` command for wrong values."""
    test_result = cli_runner.invoke(download_files, ["--recid", 0])
    assert test_result.exit_code == 2


def test_dry_run_from_doi(cli_runner):
    """Test `download-files --doi --dry-run` command."""
    test_result = cli_runner.invoke(
        download_files,
        ["--doi", "10.7483/OPENDATA.CMS.A342.9982", "--no-expand", "--dry-run"],
    )
    assert test_result.exit_code == 0
    assert (
        "CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0001_file_index.json"
        in test_result.output
    )


def test_dry_run_from_doi_wrong(cli_runner):
    """Test `download-files --doi --dry-run` command for wrong values."""
    test_result = cli_runner.invoke(
        download_files, ["--doi", "NONEXISTING", "--no-expand", "--dry-run"]
    )
    assert test_result.exit_code == 2


def test_download_files_from_doi_uses_recid_directory(cli_runner, mocker):
    """Test that download-files --doi stores files in recid directory, not 'None'."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    # DOI 10.7483/OPENDATA.CMS.W26R.J96R corresponds to recid 461
    test_file = "461/readme.txt"
    wrong_file = "None/readme.txt"
    test_result = cli_runner.invoke(
        download_files,
        ["--doi", "10.7483/OPENDATA.CMS.W26R.J96R", "--filter-name", "readme.txt"],
    )
    assert test_result.exit_code == 0
    # File should be in the recid directory (461), not 'None'
    assert os.path.isfile(test_file) is True
    assert os.path.isfile(wrong_file) is False
    assert os.path.getsize(test_file) == 2971
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_http_pycurl(cli_runner):
    """Test download_files() command with http protocol using pycurl."""
    pycurl = pytest.importorskip("pycurl")  # noqa: F841
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_http_requests(cli_runner, mocker):
    """Test download_files() command with http protocol using requests."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(download_files, ["--recid", 3005])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_https_pycurl(cli_runner):
    """Test download_files() command with https protocol using pycurl."""
    pycurl = pytest.importorskip("pycurl")  # noqa: F841
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(
        download_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_https_requests(cli_runner, mocker):
    """Test download_files() command with https protocol using requests."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(
        download_files, ["--recid", 3005, "--server", SERVER_HTTPS_URI]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_download_engine(cli_runner, mocker):
    """Test download_files() command with download-engine option."""
    mocker.patch("cernopendata_client.downloader.pycurl_available", False)
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(
        download_files, ["--recid", 3005, "--download-engine", "requests"]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_download_engine_wrong_protocol_combination_one(cli_runner):
    """Test download_files() command with download-engine option and wrong protocol."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_result = cli_runner.invoke(
        download_files,
        ["--recid", 3005, "--download-engine", "requests", "--protocol", "xrootd"],
    )
    assert test_result.exit_code == 1
    assert "requests is not compatible with xrootd" in test_result.output


def test_download_files_download_engine_wrong_protocol_combination_two(cli_runner):
    """Test download_files() command with download-engine option and wrong protocol."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_result = cli_runner.invoke(
        download_files,
        ["--recid", 3005, "--download-engine", "xrootd", "--protocol", "http"],
    )
    assert test_result.exit_code == 1
    assert "xrootd is not compatible with http" in test_result.output


def test_download_files_root(cli_runner):
    """Test download_files() command with xrootd protocol."""
    xrootd = pytest.importorskip("XRootD")  # noqa: F841
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(
        download_files, ["--recid", 3005, "--protocol", "xrootd"]
    )
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


def test_download_files_root_wrong(cli_runner, mocker):
    """Test download_files() command with xrootd protocol without xrootd."""
    mocker.patch("cernopendata_client.downloader.xrootd_available", False)
    test_result = cli_runner.invoke(
        download_files, ["--recid", 3005, "--protocol", "xrootd"]
    )
    assert test_result.exit_code == 1
    assert "xrootd is not installed on system" in test_result.output


def test_download_files_with_verify(cli_runner):
    """Test download_files() --verify command."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result = cli_runner.invoke(download_files, ["--recid", 3005, "--verify"])
    assert test_result.exit_code == 0
    assert os.path.isfile(test_file) is True
    assert os.path.getsize(test_file) == 3644
    assert test_result.output.endswith("\n==> Success!\n")


@pytest.mark.local
def test_download_files_empty_value(cli_runner):
    """Test download_files() command with empty value."""
    test_result = cli_runner.invoke(download_files)
    assert test_result.exit_code == 1
    assert "Please provide at least one of following arguments" in test_result.output


@pytest.mark.local
def test_download_files_wrong_value(cli_runner):
    """Test download_files() command with wrong value."""
    test_result = cli_runner.invoke(
        download_files,
        ["--recid", 5500, "--server", "foo"],
    )
    assert test_result.exit_code == 2
    assert "Invalid value for --server" in test_result.output


def test_download_files_filter_name(cli_runner):
    """Test download_files() command with --filter-name <name>."""
    test_file = "5500/BuildFile.xml"
    test_result_name = cli_runner.invoke(
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


def test_download_files_filter_name_multiple_values(cli_runner):
    """Test download_files() command with --filter-name <name1>,<name2>."""
    test_files = ["5500/BuildFile.xml", "5500/List_indexfile.txt"]
    test_result_name = cli_runner.invoke(
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
        assert os.path.isfile(file_location), "{} not downloaded".format(file_location)
    assert test_result_name.output.endswith("\n==> Success!\n")


def test_download_files_filter_name_wrong(cli_runner):
    """Test download_files() command with --filter-name <name> containing wrong value."""
    test_result_name = cli_runner.invoke(
        download_files, ["--recid", 5500, "--filter-name", "test_name.py"]
    )
    assert test_result_name.exit_code == 1
    assert "No files matching the filters" in test_result_name.output


def test_download_files_filter_regexp_single_file(cli_runner):
    """Test download_files() command with --filter-regexp."""
    test_file = "3005/0d0714743f0204ed3c0144941e6ce248.configFile.py"
    test_result_regexp = cli_runner.invoke(
        download_files, ["--recid", 3005, "--filter-regexp", "py$"]
    )
    assert test_result_regexp.exit_code == 0
    assert test_result_regexp.output.endswith("\n==> Success!\n")
    assert os.path.isfile(test_file), "{} not downloaded".format(test_file)


def test_download_files_filter_regexp_multiple_files(cli_runner):
    """Test download_files() command with --filter-regexp."""
    test_files = [
        "5500/HiggsDemoAnalyzer.cc",
        "5500/M4Lnormdatall.cc",
        "5500/M4Lnormdatall_lvl3.cc",
    ]
    test_result_regexp = cli_runner.invoke(
        download_files, ["--recid", 5500, "--filter-regexp", ".cc$"]
    )
    assert test_result_regexp.exit_code == 0
    for file_location in test_files:
        assert os.path.isfile(file_location), "{} not downloaded".format(file_location)
    assert test_result_regexp.output.endswith("\n==> Success!\n")


def test_download_files_filter_regexp_wrong(cli_runner):
    """Test download_files() command with --filter-regexp containing wrong value."""
    test_result_regexp_three = cli_runner.invoke(
        download_files, ["--recid", 5500, "--filter-regexp", "wontmatchanything"]
    )
    assert test_result_regexp_three.exit_code == 1
    assert "No files matching the filters" in test_result_regexp_three.output


def test_download_files_filter_range(cli_runner):
    """Test download_files() command with --filter-range <range>."""
    test_files = [
        "5500/BuildFile.xml",
        "5500/HiggsDemoAnalyzer.cc",
        "5500/List_indexfile.txt",
        "5500/M4Lnormdatall.cc",
    ]
    test_result_range = cli_runner.invoke(
        download_files, ["--recid", 5500, "--filter-range", "1-4"]
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        assert os.path.isfile(file_location), "{} not downloaded".format(file_location)
    assert test_result_range.output.endswith("\n==> Success!\n")


def test_download_files_filter_range_multiple_values(cli_runner):
    """Test download_files() command with --filter-range <range1>,<range2>."""
    test_files = [
        "5500/BuildFile.xml",
        "5500/HiggsDemoAnalyzer.cc",
        "5500/M4Lnormdatall_lvl3.cc",
        "5500/demoanalyzer_cfg_level3MC.py",
        "5500/demoanalyzer_cfg_level3data.py",
    ]
    test_result_range = cli_runner.invoke(
        download_files, ["--recid", 5500, "--filter-range", "1-2,5-7"]
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        assert os.path.isfile(file_location), "{} not downloaded".format(file_location)
    assert test_result_range.output.endswith("\n==> Success!\n")


def test_download_files_filter_single_range_single_regexp(cli_runner):
    """Test download_files() command with --filter-regexp <regexp> --filter-range <range>."""
    test_files = [
        "5500/demoanalyzer_cfg_level3MC.py",
        "5500/demoanalyzer_cfg_level3data.py",
    ]
    test_result_range = cli_runner.invoke(
        download_files,
        ["--recid", 5500, "--filter-regexp", "py", "--filter-range", "1-2"],
    )
    assert test_result_range.exit_code == 0
    for file_location in test_files:
        assert os.path.isfile(file_location), "{} not downloaded".format(file_location)
    assert test_result_range.output.endswith("\n==> Success!\n")


def test_download_files_filter_multiple_range_single_regexp(cli_runner):
    """Test download_files() command with --filter-regexp <regexp> --filter-range <range1>,<range2>."""
    test_files = [
        "5500/demoanalyzer_cfg_level3MC.py",
        "5500/demoanalyzer_cfg_level3data.py",
        "5500/demoanalyzer_cfg_level4data.py",
    ]
    test_result_range = cli_runner.invoke(
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
        assert os.path.isfile(file_location), "{} not downloaded".format(file_location)
    assert test_result_range.output.endswith("\n==> Success!\n")
