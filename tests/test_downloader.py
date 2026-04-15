# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2025, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client downloader unit tests."""

import pytest

from cernopendata_client.downloader import (
    get_download_files_by_name,
    get_download_files_by_regexp,
    get_download_files_by_range,
    get_file_subdirectories,
)


@pytest.mark.local
def test_get_download_files_by_name_single():
    """Test filtering files by a single name."""
    file_locations = [
        "http://example.com/a.txt",
        "http://example.com/b.txt",
        "http://example.com/c.py",
    ]
    result = get_download_files_by_name(names=["a.txt"], file_locations=file_locations)
    assert result == ["http://example.com/a.txt"]


@pytest.mark.local
def test_get_download_files_by_name_multiple():
    """Test filtering files by multiple names."""
    file_locations = [
        "http://example.com/a.txt",
        "http://example.com/b.txt",
        "http://example.com/c.py",
    ]
    result = get_download_files_by_name(
        names=["a.txt", "c.py"], file_locations=file_locations
    )
    assert result == ["http://example.com/a.txt", "http://example.com/c.py"]


@pytest.mark.local
def test_get_download_files_by_name_no_match():
    """Test filtering files by name with no matches."""
    file_locations = [
        "http://example.com/a.txt",
        "http://example.com/b.txt",
    ]
    result = get_download_files_by_name(
        names=["nonexistent.txt"], file_locations=file_locations
    )
    assert result == []


@pytest.mark.local
def test_get_download_files_by_regexp_extension():
    """Test filtering files by regexp matching extension."""
    file_locations = [
        "http://example.com/a.py",
        "http://example.com/b.txt",
        "http://example.com/c.py",
    ]
    result = get_download_files_by_regexp(
        regexp=r"\.py$", file_locations=file_locations
    )
    assert result == ["http://example.com/a.py", "http://example.com/c.py"]


@pytest.mark.local
def test_get_download_files_by_regexp_pattern():
    """Test filtering files by regexp pattern."""
    file_locations = [
        "http://example.com/test_001.dat",
        "http://example.com/test_002.dat",
        "http://example.com/other.dat",
    ]
    result = get_download_files_by_regexp(
        regexp=r"test_\d+", file_locations=file_locations
    )
    assert result == [
        "http://example.com/test_001.dat",
        "http://example.com/test_002.dat",
    ]


@pytest.mark.local
def test_get_download_files_by_regexp_with_filtered_files():
    """Test filtering files by regexp with pre-filtered files."""
    file_locations = [
        "http://example.com/a.py",
        "http://example.com/b.py",
        "http://example.com/c.txt",
    ]
    filtered_files = ["http://example.com/a.py", "http://example.com/c.txt"]
    result = get_download_files_by_regexp(
        regexp=r"\.py$", file_locations=file_locations, filtered_files=filtered_files
    )
    assert result == ["http://example.com/a.py"]


@pytest.mark.local
def test_get_download_files_by_regexp_no_match():
    """Test filtering files by regexp with no matches."""
    file_locations = [
        "http://example.com/a.txt",
        "http://example.com/b.txt",
    ]
    result = get_download_files_by_regexp(
        regexp=r"\.py$", file_locations=file_locations
    )
    assert result == []


@pytest.mark.local
def test_get_download_files_by_range_single():
    """Test filtering files by a single range."""
    file_locations = [
        "http://example.com/file1.txt",
        "http://example.com/file2.txt",
        "http://example.com/file3.txt",
        "http://example.com/file4.txt",
        "http://example.com/file5.txt",
    ]
    result = get_download_files_by_range(ranges=["2-4"], file_locations=file_locations)
    assert result == [
        "http://example.com/file2.txt",
        "http://example.com/file3.txt",
        "http://example.com/file4.txt",
    ]


@pytest.mark.local
def test_get_download_files_by_range_multiple():
    """Test filtering files by multiple ranges."""
    file_locations = [
        "http://example.com/file1.txt",
        "http://example.com/file2.txt",
        "http://example.com/file3.txt",
        "http://example.com/file4.txt",
        "http://example.com/file5.txt",
    ]
    result = get_download_files_by_range(
        ranges=["1-2", "4-5"], file_locations=file_locations
    )
    assert result == [
        "http://example.com/file1.txt",
        "http://example.com/file2.txt",
        "http://example.com/file4.txt",
        "http://example.com/file5.txt",
    ]


@pytest.mark.local
def test_get_download_files_by_range_single_file():
    """Test filtering files by range selecting a single file."""
    file_locations = [
        "http://example.com/file1.txt",
        "http://example.com/file2.txt",
        "http://example.com/file3.txt",
    ]
    result = get_download_files_by_range(ranges=["2-2"], file_locations=file_locations)
    assert result == ["http://example.com/file2.txt"]


@pytest.mark.local
def test_get_download_files_by_range_with_filtered_files():
    """Test filtering files by range with pre-filtered files."""
    file_locations = [
        "http://example.com/file1.txt",
        "http://example.com/file2.txt",
        "http://example.com/file3.txt",
    ]
    filtered_files = ["http://example.com/file1.txt", "http://example.com/file3.txt"]
    result = get_download_files_by_range(
        ranges=["1-2"], file_locations=file_locations, filtered_files=filtered_files
    )
    assert result == ["http://example.com/file1.txt", "http://example.com/file3.txt"]


@pytest.mark.local
def test_get_file_subdirectories_unique_names():
    """Test that unique file names produce no subdirectories."""
    file_locations = [
        "http://example.com/dir1/a.txt",
        "http://example.com/dir2/b.txt",
        "http://example.com/dir3/c.txt",
    ]
    result = get_file_subdirectories(file_locations)
    assert all(subdir == "" for subdir in result.values())


@pytest.mark.local
def test_get_file_subdirectories_duplicate_names_one_level():
    """Test that duplicate names with different parent dirs use one level."""
    file_locations = [
        "http://opendata.cern.ch/eos/opendata/alice/2015/LHC15o/000245349/0002/AO2D.root",
        "http://opendata.cern.ch/eos/opendata/alice/2015/LHC15o/000245349/0003/AO2D.root",
        "http://opendata.cern.ch/eos/opendata/alice/2015/LHC15o/000245349/0004/AO2D.root",
    ]
    result = get_file_subdirectories(file_locations)
    assert result[file_locations[0]] == "0002"
    assert result[file_locations[1]] == "0003"
    assert result[file_locations[2]] == "0004"


@pytest.mark.local
def test_get_file_subdirectories_duplicate_names_two_levels():
    """Test that deeper disambiguation uses multiple directory levels."""
    file_locations = [
        "http://opendata.cern.ch/eos/opendata/alice/000245349/0002/AO2D.root",
        "http://opendata.cern.ch/eos/opendata/alice/000245350/0002/AO2D.root",
    ]
    result = get_file_subdirectories(file_locations)
    assert result[file_locations[0]] == "000245349/0002"
    assert result[file_locations[1]] == "000245350/0002"


@pytest.mark.local
def test_get_file_subdirectories_mixed_duplicates():
    """Test mixed unique and duplicate file names."""
    file_locations = [
        "http://example.com/dir1/0001/data.root",
        "http://example.com/dir1/0002/data.root",
        "http://example.com/dir1/unique.txt",
    ]
    result = get_file_subdirectories(file_locations)
    # Common prefix is "http://example.com/dir1", so subdirs are relative to that
    assert result[file_locations[0]] == "0001"
    assert result[file_locations[1]] == "0002"
    assert result[file_locations[2]] == ""


@pytest.mark.local
def test_get_file_subdirectories_varying_depths():
    """Test files at varying directory depths with common prefix stripping."""
    file_locations = [
        "http://opendata.cern.ch/eos/opendata/alice/mydata/foo/bar/data.root",
        "http://opendata.cern.ch/eos/opendata/alice/mydata/data.root",
        "http://opendata.cern.ch/eos/opendata/alice/mydata/foo/baz/data.root",
        "http://opendata.cern.ch/eos/opendata/alice/mydata/foo/data.root",
    ]
    result = get_file_subdirectories(file_locations)
    # Common prefix is "http://opendata.cern.ch/eos/opendata/alice/mydata"
    assert result[file_locations[0]] == "foo/bar"
    assert result[file_locations[1]] == ""
    assert result[file_locations[2]] == "foo/baz"
    assert result[file_locations[3]] == "foo"


@pytest.mark.local
def test_get_file_subdirectories_empty_list():
    """Test with an empty file list."""
    result = get_file_subdirectories([])
    assert result == {}
