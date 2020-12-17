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
    if recid is None:
        display_message(
            msg_type="error",
            msg="You must supply a record ID number as an " "input using -r flag.",
        )
        sys.exit(1)
    if recid <= 0:
        display_message(
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
    server = server.split(":")
    if server[0] not in ["http", "https"]:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Server should be a valid HTTP/HTTPS URI".format(
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
        range_from, range_to = int(range.split("-")[0]), int(range.split("-")[-1])
    except Exception:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Range should have start and end index(i-j)".format(
                "--filter-range", range
            ),
        )
        sys.exit(2)
    if range_from <= 0:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Range should start from a positive integer".format(
                "--filter-range", range_from
            ),
        )
        sys.exit(2)
    if range_to > count:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Range is too big. There are total {} files".format(
                "--filter-range", range, count
            ),
        )
        sys.exit(2)
    if range_to < range_from:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Range is not valid".format(
                "--filter-range", range
            ),
        )
        sys.exit(2)
    return True


def validate_directory(directory=None):
    """Return True if directory path is correct, exit otherwise.

    :param directory: EOSPUBLIC path

    :return: Bool after verifying directory
    :rtype: bool
    """
    if sys.version_info[0] < 3:
        if isinstance(directory, unicode):  # noqa F821
            directory = directory.encode("utf-8")
    if isinstance(directory, str):
        if not directory.startswith("/eos/opendata/"):
            display_message(
                msg_type="error",
                msg="Invalid value for directory. {} is not valid EOSPUBLIC path".format(
                    directory
                ),
            )
            sys.exit(2)
    else:
        display_message(
            msg_type="error",
            msg="Invalid directory. {} is not valid string".format(directory),
        )
        sys.exit(2)
    return True


def validate_retry_limit(retry_limit=None):
    """Return True if retry_limit is valid, exit otherwise.

    :param retry_limit: Number of retries when downloading a file.

    :return: Bool after verifying retry_limit
    :rtype: bool
    """
    if retry_limit is None:
        display_message(
            msg_type="error",
            msg="You must supply a number input using --retry-limit flag.",
        )
        sys.exit(1)
    if retry_limit <= 0:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Retry limit should be a positive integer".format(
                "--retry-limit", retry_limit
            ),
        )
        sys.exit(2)
    return True


def validate_retry_sleep(retry_sleep=None):
    """Return True if retry_sleep is valid, exit otherwise.

    :param retry_sleep: Sleep time in seconds before retrying downloads.

    :return: Bool after verifying retry_sleep
    :rtype: bool
    """
    if retry_sleep is None:
        display_message(
            msg_type="error",
            msg="You must supply a number input using --retry-sleep flag.",
        )
        sys.exit(1)
    if retry_sleep <= 0:
        display_message(
            msg_type="error",
            msg="Invalid value for {}: {} - Retry sleep should be a positive integer".format(
                "--retry-sleep", retry_sleep
            ),
        )
        sys.exit(2)
    return True
