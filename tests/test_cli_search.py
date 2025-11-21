# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client cli command search test."""

from click.testing import CliRunner
from cernopendata_client.cli import search


def test_search_command():
    """Test `search` command."""
    runner = CliRunner()
    result = runner.invoke(
        search,
        [
            "--q",
            "Higgs",
            "--experiment",
            "CMS",
            "--year",
            "2012--2012",
            "--type",
            "Dataset",
            "--category",
            "Higgs Physics",
        ],
    )
    assert result.exit_code == 0
    assert "Summer12" in result.output or "2012" in result.output
    assert "/" in result.output
    assert (
        "AODSIM" in result.output
        or "MINIAODSIM" in result.output
        or "NANOAODSIM" in result.output
    )


def test_search_command_with_query_url():
    """Test `search` command with --query URL option."""
    runner = CliRunner()
    result = runner.invoke(
        search,
        [
            "--query",
            "q=Higgs&f=experiment%3ACMS",
        ],
    )
    assert result.exit_code == 0


def test_search_command_with_query_pattern():
    """Test `search` command with --query-pattern option."""
    runner = CliRunner()
    result = runner.invoke(
        search,
        [
            "--query-pattern",
            "muon",
        ],
    )
    assert result.exit_code == 0


def test_search_command_with_query_facet():
    """Test `search` command with --query-facet option."""
    runner = CliRunner()
    result = runner.invoke(
        search,
        [
            "--query-pattern",
            "test",
            "--query-facet",
            "experiment",
            "CMS",
            "--query-facet",
            "type",
            "Dataset",
        ],
    )
    assert result.exit_code == 0


def test_search_command_mixed_options():
    """Test `search` command mixing new and legacy options."""
    runner = CliRunner()
    result = runner.invoke(
        search,
        [
            "--query-pattern",
            "Higgs",
            "--experiment",
            "CMS",
        ],
    )
    assert result.exit_code == 0
