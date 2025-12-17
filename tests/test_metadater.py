# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file metadater test."""

import pytest

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
            "inspireid=INSPIRE-00330082",
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


@pytest.mark.local
def test_filter_matching_output_without_output_field(capsys):
    """Test filter_matching_output when output_field is not in object."""
    matching_objects = {"name_0": {"foo": "bar", "baz": "qux"}}
    output_json = [{"foo": "bar", "baz": "qux"}]
    filter_matching_output(matching_objects, "nonexistent", output_json)
    captured = capsys.readouterr()
    assert '"foo": "bar"' in captured.out
    assert '"baz": "qux"' in captured.out


@pytest.mark.local
def test_filter_matching_output_multiple_matches_without_output_field(capsys):
    """Test filter_matching_output with multiple matches when output_field is not in object."""
    # Two different filter fields matching the same object at index 0
    matching_objects = {
        "field1_0": {"a": "1", "b": "2"},
        "field2_0": {"a": "1", "b": "2"},
    }
    output_json = [{"a": "1", "b": "2"}]
    filter_matching_output(matching_objects, "nonexistent", output_json)
    captured = capsys.readouterr()
    assert '"a": "1"' in captured.out
    assert '"b": "2"' in captured.out


@pytest.mark.local
def test_filter_metadata_schema_field():
    """Test filter_metadata when output_json contains $schema."""
    output_json = ["$schema", {"name": "test"}]
    with pytest.raises(SystemExit) as exc_info:
        filter_metadata("name", ["name=test"], output_json)
    assert exc_info.value.code == 1
