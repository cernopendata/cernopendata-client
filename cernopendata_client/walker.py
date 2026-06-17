# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client EOSPUBLIC filesystem related utilities."""

from __future__ import print_function

import os
import sys
import datetime

from .config import SERVER_ROOT_URI
from .printer import display_message

# XRootD client error code for a not-found path. Resolved at import time and
# left as None for older bindings that do not expose it; the wire-protocol
# errno below is the stable fallback.
XROOTD_CODE_NOT_FOUND = None

try:
    from XRootD import client as xrootdclient
    from XRootD.client.flags import DirListFlags
    from XRootD.client.responses import XRootDStatus

    XROOTD_CODE_NOT_FOUND = getattr(XRootDStatus, "errNotFound", None)
    FS = xrootdclient.FileSystem(SERVER_ROOT_URI)
    xrootd_available = True
except ImportError:
    xrootd_available = False

# XRootD server error number returned when a path does not exist (kXR_NotFound).
XROOTD_ERRNO_NOT_FOUND = 3011


def get_list_directory(path, recursive, timeout, time_start=None):
    """Return list of contents of a EOSPUBLIC Open Data directory.

    :param path: EOSPUBLIC path
    :param recursive: Iterate recursively into subdirectories?
    :param timeout: Timeout for list-directory command.
    :param time_start: Optionally, time When the recursive search started.
    :type path: str
    :type recursive: bool
    :type timeout: int
    :type time_start: datetime

    :return: List of files
    :rtype: list
    """
    if not xrootd_available:
        display_message(
            msg_type="error",
            msg="xrootd is required for this operation but it is not installed on your system.",
        )
        sys.exit(1)
    if not time_start:
        time_start = datetime.datetime.now()
    if (datetime.datetime.now() - time_start).seconds > timeout:
        display_message(
            msg_type="error",
            msg="Command timed out. Please increase timeout or provide more specific path.",
        )
        sys.exit(2)
    files = []
    status, listing = FS.dirlist(path, DirListFlags.STAT)
    if not status.ok:
        # A missing path is reported via the stable server error number, or,
        # when the binding exposes it, the client-level not-found code.
        path_not_found = status.errno == XROOTD_ERRNO_NOT_FOUND or (
            XROOTD_CODE_NOT_FOUND is not None and status.code == XROOTD_CODE_NOT_FOUND
        )
        if path_not_found:
            display_message(
                msg_type="error",
                msg="Directory {} does not exist.".format(path),
            )
        else:
            display_message(
                msg_type="error",
                msg="Cannot list directory {}: {}".format(path, status.message.strip()),
            )
        sys.exit(1)
    for entry in listing:
        if entry.statinfo.flags == 19:  # entry is a directory
            files.append(path + os.sep + entry.name)
            if recursive:
                files.extend(
                    get_list_directory(
                        path + os.sep + entry.name, recursive, timeout, time_start
                    )
                )
        else:
            files.append(path + os.sep + entry.name)
    return files
