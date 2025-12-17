# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client downloader unit tests."""

import pytest

from cernopendata_client.downloader import (
    get_download_files_by_name,
    get_download_files_by_regexp,
    get_download_files_by_range,
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
