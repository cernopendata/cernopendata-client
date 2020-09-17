# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

import click


def validate_recid(recid=None):
    """Validate record ID.

    Returns True if OK, raises click.BadParameter exception otherwise.
    """
    if recid <= 0:
        raise click.BadParameter(
            "Recid should be a positive integer",
            param_hint=["--recid"],
        )
    return True


def validate_server(server=None):
    """Validate server URL.

    Returns True if OK, raises click.BadParameter exception otherwise.
    """
    if not server.startswith("http://"):
        raise click.BadParameter(
            "Server should be a valid URL",
            param_hint=["--server"],
        )
    return True


def validate_range(range=None, count=None):
    """Validate filter range.

    Return True if range lies in total files count,
    raises click.BadParameter exception otherwise.
    """
    if len(range.split("-")) != 2:
        raise click.BadParameter(
            "Range should have start and end index(i-j)",
            param_hint=["--filter-range"],
        )
    range_from, range_to = int(range.split("-")[0]), int(range.split("-")[-1])
    if range_from <= 0:
        raise click.BadParameter(
            "Range should start from a positive integer",
            param_hint=["--filter-range"],
        )
    if range_to > count:
        raise click.BadParameter(
            "Range is too big",
            param_hint=["--filter-range"],
        )
    if range_to < range_from:
        raise click.BadParameter(
            "Range is not valid",
            param_hint=["--filter-range"],
        )
    return True
