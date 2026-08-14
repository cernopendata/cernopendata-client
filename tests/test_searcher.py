# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client searcher unit tests."""

import pytest

from cernopendata_client.searcher import get_file_entries, get_files_list


@pytest.fixture
def record_with_file_index():
    """Return representative direct-file and file-index metadata."""
    return {
        "metadata": {
            "recid": "42",
            "files": [
                {
                    "uri": "root://eospublic.cern.ch//eos/direct.txt",
                    "size": 6,
                    "checksum": "adler32:087e0289",
                }
            ],
            "_file_indices": [
                {
                    "key": "index.json",
                    "size": 1000000,
                    "files": [
                        {
                            "uri": "root://eospublic.cern.ch//eos/0001/data.root",
                            "size": 5,
                            "checksum": "adler32:062c0215",
                        },
                        {
                            "uri": "root://eospublic.cern.ch//eos/0002/data.root",
                            "size": 6,
                            "checksum": "adler32:08ca027d",
                        },
                    ],
                }
            ],
        }
    }


@pytest.mark.local
def test_get_file_entries_marks_only_unexpanded_index(record_with_file_index):
    """Test expanded files retain normal size and checksum verification."""
    entries = get_file_entries(
        "http://opendata.cern.ch",
        record_with_file_index,
        protocol="http",
        expand=True,
    )

    assert len(entries) == 3
    assert all(not entry.is_file_index for entry in entries)
    assert [entry.size for entry in entries] == [6, 5, 6]


@pytest.mark.local
def test_get_file_entries_marks_unexpanded_index(record_with_file_index):
    """Test a synthetic file-index response has an explicit origin marker."""
    entries = get_file_entries(
        "http://opendata.cern.ch",
        record_with_file_index,
        protocol="http",
        expand=False,
    )

    assert len(entries) == 2
    assert entries[1].is_file_index is True
    assert entries[1].size == 1000000
    assert entries[1].checksum == ""
    assert entries[1].uri.endswith("/record/42/file_index/index.json")


@pytest.mark.local
def test_get_files_list_preserves_public_tuple_shape(record_with_file_index):
    """Test the public file-list helper remains backwards compatible."""
    files = get_files_list(
        "http://opendata.cern.ch",
        record_with_file_index,
        protocol="http",
        expand=False,
    )

    assert all(isinstance(file_info, tuple) for file_info in files)
    assert all(len(file_info) == 3 for file_info in files)


@pytest.mark.local
def test_get_file_entries_allows_missing_checksum():
    """Test files without checksum metadata still receive size validation."""
    record = {
        "metadata": {
            "recid": "42",
            "files": [{"uri": "root://eospublic.cern.ch//eos/data.bin", "size": 4}],
        }
    }

    entry = get_file_entries(
        "http://opendata.cern.ch", record, protocol="http", expand=True
    )[0]

    assert entry.size == 4
    assert entry.checksum == ""
