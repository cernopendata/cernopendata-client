# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client utils test."""

import click
import pytest

from cernopendata_client.utils import parse_parameters, parse_query_from_url


@pytest.mark.local
def test_parse_parameters():
    """Test parse_parameters() method."""
    pytest.raises(SystemExit, parse_parameters, (9))
    assert parse_parameters(("test.py",)) == ["test.py"]
    assert parse_parameters(("2-4,9-12",)) == ["2-4", "9-12"]


def test_parse_query_from_url_full_url():
    """Test parse_query_from_url() with full URL."""
    url = "https://opendata.cern.ch/search?q=muon&f=experiment%3ACMS&p=1&s=10"
    result = parse_query_from_url(url)
    assert result["q"] == "muon"
    assert result["facets"]["experiment"] == "CMS"
    assert result["page"] == 1
    assert result["size"] == 10


def test_parse_query_from_url_query_string():
    """Test parse_query_from_url() with query string."""
    query = "q=Higgs&f=type%3ADataset&f=experiment%3ACMS"
    result = parse_query_from_url(query)
    assert result["q"] == "Higgs"
    assert result["facets"]["type"] == "Dataset"
    assert result["facets"]["experiment"] == "CMS"


def test_parse_query_from_url_multiple_facets():
    """Test parse_query_from_url() with multiple facets."""
    query = "f=experiment%3ACMS&f=type%3ADataset&f=year%3A2012"
    result = parse_query_from_url(query)
    assert result["facets"]["experiment"] == "CMS"
    assert result["facets"]["type"] == "Dataset"
    assert result["facets"]["year"] == "2012"


def test_parse_query_from_url_empty():
    """Test parse_query_from_url() with empty input."""
    result = parse_query_from_url("")
    assert result["q"] == ""
    assert result["facets"] == {}
    assert result["page"] is None
    assert result["size"] is None


def test_parse_query_from_url_sort():
    """Test parse_query_from_url() with sort parameter."""
    query = "q=test&sort=mostrecent"
    result = parse_query_from_url(query)
    assert result["q"] == "test"
    assert result["sort"] == "mostrecent"


def test_parse_query_from_url_size_parameter():
    """Test parse_query_from_url() with size parameter."""
    query = "q=test&size=20"
    result = parse_query_from_url(query)
    assert result["size"] == 20


def test_parse_query_from_url_invalid_page():
    """Test parse_query_from_url() with invalid page parameter."""
    query = "q=test&p=invalid"
    result = parse_query_from_url(query)
    assert result["page"] is None
