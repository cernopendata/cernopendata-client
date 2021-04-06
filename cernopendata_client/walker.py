# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021 CERN.
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

try:
    from XRootD import client as xrootdclient
    from XRootD.client.flags import DirListFlags

    FS = xrootdclient.FileSystem(SERVER_ROOT_URI)
    xrootd_available = True
except ImportError:
    xrootd_available = False


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
    try:
        status, listing = FS.dirlist(path, DirListFlags.STAT)
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
    except Exception:
        display_message(
            msg_type="error",
            msg="Directory {} does not exist.".format(path),
        )
        sys.exit(1)
    return files
