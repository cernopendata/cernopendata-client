# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client input validation methods."""

import click
import sys

from .printer import display_message


def validate_recid(recid=None):
    """Return True if record ID is valid, exit otherwise.

    :param recid: Record ID
    :type recid: int

    :return: Bool after verifying record ID
    :rtype: bool
    """
    if recid <= 0:
        display_message(
            prefix="double",
            msg_type="error",
            msg="Invalid value for {}: {} - Recid should be a positive integer".format(
                "--recid", recid
            ),
        )
        sys.exit(2)
    return True


def validate_server(server=None):
    """Return True if server uri is valid, exit otherwise.

    :param server: CERN Open Data server to query
    :type server: str

    :return: Bool after verfying server url
    :rtype: bool
    """
    if not server.startswith("http://"):
        display_message(
            prefix="double",
            msg_type="error",
            msg="Invalid value for {}: {} - Server should be a valid HTTP URI".format(
                "--server", server
            ),
        )
        sys.exit(2)
    return True


def validate_range(range=None, count=None):
    """Return True if range lies in total files count, exit otherwise.

    :param range: Range of files indexes
    :param count: Total files in a record
    :type range: str
    :type count: int

    :return: Bool after verifying range
    :rtype: bool
    """
    try:
        if len(range.split("-")) != 2:
            display_message(
                prefix="double",
                msg_type="error",
                msg="Invalid value for {}: {} - Range should have start and end index(i-j)".format(
                    "--filter-range", range
                ),
            )
            sys.exit(2)
        range_from, range_to = int(range.split("-")[0]), int(range.split("-")[-1])
    except Exception:
        display_message(
            prefix="double",
            msg_type="error",
            msg="Invalid value for {}: {} - Range should have start and end index(i-j)".format(
                "--filter-range", range
            ),
        )
        sys.exit(2)
    if range_from <= 0:
        display_message(
            prefix="double",
            msg_type="error",
            msg="Invalid value for {}: {} - Range should start from a positive integer".format(
                "--filter-range", range_from
            ),
        )
        sys.exit(2)
    if range_to > count:
        display_message(
            prefix="double",
            msg_type="error",
            msg="Invalid value for {}: {} - Range is too big. There are total {} files".format(
                "--filter-range", range, count
            ),
        )
        sys.exit(2)
    if range_to < range_from:
        display_message(
            prefix="double",
            msg_type="error",
            msg="Invalid value for {}: {} - Range is not valid".format(
                "--filter-range", range
            ),
        )
        sys.exit(2)
    return True
