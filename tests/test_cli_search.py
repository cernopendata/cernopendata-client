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
    assert "/GluGluTohhTo4b_non-resonant-mh-125_8TeV-madgraph-pythia6-tauola/Summer12_DR53X-PU_S10_START53_V19-v1/AODSIM" in result.output

