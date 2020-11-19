# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client EOSPUBLIC filesystem related utilities."""

from __future__ import print_function

import sys
import datetime

from .config import SERVER_ROOT_URI
from .printer import display_message

try:
    from xrootdpyfs import XRootDPyFS

    xrootd_available = True
except ImportError:
    xrootd_available = False


def get_list_directory_recursive(path, timeout):
    """Return list of contents of a EOSPUBLIC Open Data directory recursively.

    :param path: EOSPUBLIC path
    :type path: str

    :return: List of files
    :rtype: list
    """
    files_list = []
    timeout_flag = False
    start_time = datetime.datetime.now()
    fs = XRootDPyFS("root://eospublic.cern.ch//")
    try:
        for dirs, files in fs.walk(path):
            current_time = datetime.datetime.now()
            elapsed_time = current_time - start_time
            if elapsed_time.seconds > timeout:
                timeout_flag = True
                break
            else:
                for _file in files:
                    files_list.append(_file)
        return files_list, timeout_flag
    except Exception:
        display_message(
            msg_type="error",
            msg="Directory {} does not exist.".format(path),
        )
        sys.exit(1)


def get_list_directory(path, recursive, timeout):
    """Return list of contents of a EOSPUBLIC Open Data directory.

    :param path: EOSPUBLIC path
    :param recursive: Iterate recurcively in the given directory path.
    :param timeout: Timeout for list-directory command.
    :type path: str
    :type recursive: bool
    :type timeout: int

    :return: List of files
    :rtype: list
    """
    if not xrootd_available:
        display_message(
            msg_type="error",
            msg="xrootd is required for this operation but it is not installed on your system.",
        )
        sys.exit(1)
    if not recursive:
        directory = SERVER_ROOT_URI + path
        fs = XRootDPyFS(directory)
        try:
            files_list = fs.listdir()
            return files_list
        except Exception:
            display_message(
                msg_type="error",
                msg="Directory {} does not exist.".format(path),
            )
            sys.exit(1)
    else:
        files_list, timeout_flag = get_list_directory_recursive(path, timeout)
        if timeout_flag:
            display_message(
                msg_type="error",
                msg="Command timed out. Please provide more specific path.",
            )
            sys.exit(2)
        return files_list
