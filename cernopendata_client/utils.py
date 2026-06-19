# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client utility functions."""

import click
import sys
from urllib.parse import urlparse, parse_qs, unquote

from .printer import display_message


def parse_parameters(filter_input):
    """Return parsed filter parameters.

    :param filter_input: Tuple of filters input
    :type filter_input: tuple

    :return: List of filters separated by commas
    :rtype: list
    """
    try:
        filters = " ".join(filter_input).split(",")
        return filters
    except Exception:
        display_message(
            msg_type="error",
            msg="{} - Wrong input format".format(filter_input),
        )
        sys.exit(2)


def parse_query_from_url(query_input):
    """Parse query parameters from a URL or query string.

    Extract search parameters from a CERN Open Data search URL or query string.
    Handles URL-encoded parameters and facet parsing.

    :param query_input: Full URL or query string
    :type query_input: str

    :return: Dictionary containing 'q' (query pattern), 'facets' (dict), 'page', 'size', 'sort'
    :rtype: dict
    """
    result = {
        "q": "",
        "facets": {},
        "page": None,
        "size": None,
        "sort": None,
    }

    try:
        if query_input.startswith("http://") or query_input.startswith("https://"):
            parsed_url = urlparse(query_input)
            query_string = parsed_url.query
        else:
            query_string = query_input

        params = parse_qs(query_string)

        if "q" in params:
            result["q"] = params["q"][0] if params["q"] else ""

        if "f" in params:
            for facet_string in params["f"]:
                facet_string = unquote(facet_string)
                if ":" in facet_string:
                    facet_key, facet_value = facet_string.split(":", 1)
                    result["facets"][facet_key] = facet_value

        if "p" in params:
            try:
                result["page"] = int(params["p"][0])
            except (ValueError, IndexError):
                pass

        if "s" in params or "size" in params:
            size_param = params.get("s", params.get("size", []))
            if size_param:
                try:
                    result["size"] = int(size_param[0])
                except (ValueError, IndexError):
                    pass

        if "sort" in params:
            result["sort"] = params["sort"][0]

        return result

    except Exception as e:
        display_message(
            msg_type="error",
            msg="Failed to parse query: {} - {}".format(query_input, str(e)),
        )
        sys.exit(2)
