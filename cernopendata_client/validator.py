# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client input validation methods."""

import click

from .printer import display_message


def validate_recid(recid=None):
    """Return True if OK, raises click.BadParameter exception otherwise.

    :param recid: Record ID
    :type recid: int

    :return: Bool after verifying record ID
    :rtype: bool
    """
    if recid <= 0:
        raise click.BadParameter(
            "{}".format(
                display_message(
                    prefix="double",
                    msg_type="error",
                    msg="Recid should be a positive integer",
                )
            ),
            param_hint=["--recid"],
        )
    return True


def validate_server(server=None):
    """Return True if OK, raises click.BadParameter exception otherwise.

    :param server: CERN Open Data server to query
    :type server: str

    :return: Bool after verfying server url
    :rtype: bool
    """
    if not server.startswith("http://"):
        raise click.BadParameter(
            "{}".format(
                display_message(
                    prefix="double",
                    msg_type="error",
                    msg="Server should be a valid URL",
                )
            ),
            param_hint=["--server"],
        )
    return True


def validate_range(range=None, count=None):
    """Return True if range lies in total files count.

    :param range: Range of files indexes
    :param count: Total files in a record
    :type range: str
    :type count: int

    :return: Bool after verifying range
    :rtype: bool
    """
    try:
        if len(range.split("-")) != 2:
            raise click.BadParameter(
                "{}".format(
                    display_message(
                        prefix="double",
                        msg_type="error",
                        msg="Range should have start and end index(i-j)",
                    )
                ),
                param_hint=["--filter-range"],
            )
        range_from, range_to = int(range.split("-")[0]), int(range.split("-")[-1])
    except Exception:
        raise click.BadParameter(
            "{}".format(
                display_message(
                    prefix="double",
                    msg_type="error",
                    msg="Range should have start and end index(i-j)",
                )
            ),
            param_hint=["--filter-range"],
        )
    if range_from <= 0:
        raise click.BadParameter(
            "{}".format(
                display_message(
                    prefix="double",
                    msg_type="error",
                    msg="Range should start from a positive integer",
                )
            ),
            param_hint=["--filter-range"],
        )
    if range_to > count:
        raise click.BadParameter(
            "{}".format(
                display_message(
                    prefix="double", msg_type="error", msg="Range is too big"
                )
            ),
            param_hint=["--filter-range"],
        )
    if range_to < range_from:
        raise click.BadParameter(
            "{}".format(
                display_message(
                    prefix="double", msg_type="error", msg="Range is not valid"
                )
            ),
            param_hint=["--filter-range"],
        )
    return True
