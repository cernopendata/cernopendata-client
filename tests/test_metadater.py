# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file metadater test."""

from click.testing import CliRunner
from cernopendata_client.cli import get_metadata

from cernopendata_client.metadater import (
    filter_metadata,
    filter_matching_output,
)


def test_get_metadata_from_filter_fields_empty():
    """Test `get-metadata --recid --output-value --filter` command with empty values."""
    test_get_metadata = CliRunner()
    test_result = test_get_metadata.invoke(
        get_metadata,
        ["--recid", 1, "--output-value", "usage.links.description", "--filter", "url"],
    )
    assert test_result.exit_code == 1
    assert (
        "Invalid filter format. Use --filter some_field_name=some_value"
        in test_result.output
    )


def test_get_metadata_from_filter_metadata_one():
    """Test `get-metadata --recid --output-value --filter` command."""
    test_get_metadata = CliRunner()
    test_result = test_get_metadata.invoke(
        get_metadata,
        [
            "--recid",
            1,
            "--output-value",
            "usage.links.description",
            "--filter",
            "url=/docs/cms-getting-started-2010",
        ],
    )
    assert test_result.exit_code == 0
    assert "Getting started with CMS open data" in test_result.output


def test_get_metadata_from_filter_metadata_two():
    """Test `get-metadata --recid --output-value --filter` command."""
    test_get_metadata = CliRunner()
    test_result = test_get_metadata.invoke(
        get_metadata,
        [
            "--recid",
            451,
            "--output-value",
            "authors.name",
            "--filter",
            "affiliation=CERN",
            "--filter",
            "ccid=CCID-722528",
        ],
    )
    assert test_result.exit_code == 0
    assert "Plagge, Michael" in test_result.output


def test_get_metadata_from_filter_metadata_wrong_one():
    """Test `get-metadata --recid --output-value --filter` command for wrong values."""
    test_get_metadata = CliRunner()
    test_result = test_get_metadata.invoke(
        get_metadata,
        [
            "--recid",
            1,
            "--output-value",
            "usage.links.description",
            "--filter",
            "link=/docs/cms-getting-started-2010",
        ],
    )
    assert test_result.exit_code == 1
    assert "Field 'link' is not present in metadata" in test_result.output


def test_get_metadata_from_filter_metadata_wrong_two():
    """Test `get-metadata --recid --output-value --filter` command for wrong values."""
    test_get_metadata = CliRunner()
    test_result = test_get_metadata.invoke(
        get_metadata,
        [
            "--recid",
            1,
            "--output-value",
            "usage.links.description",
            "--filter",
            "url=/docs/cms-getting-started-20",
        ],
    )
    assert test_result.exit_code == 1
    assert (
        "No objects found with url=/docs/cms-getting-started-20" in test_result.output
    )
