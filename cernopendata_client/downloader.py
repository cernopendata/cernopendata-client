# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file downloading related utilities."""

import sys
import os
import re
import time
import requests

try:
    import pycurl

    pycurl_available = True
except ImportError:
    pycurl_available = False

try:
    from xrootdpyfs import XRootDPyFS

    xrootd_available = True
except ImportError:
    xrootd_available = False

from .validator import validate_range
from .printer import display_message
from .verifier import get_file_checksum
from .config import DOWNLOAD_ERROR_PAGE


def check_error(
    path=None, file_location=None, protocol=None, retry_limit=None, retry_sleep=None
):
    """Check downloaded file for error page."""
    file_name = file_location.split("/")[-1]
    file_path = path + "/" + file_name
    downloaded_file = {
        "size": os.path.getsize(file_path),
        "checksum": get_file_checksum(file_path),
    }
    if (
        DOWNLOAD_ERROR_PAGE["size"] == downloaded_file["size"]
        and DOWNLOAD_ERROR_PAGE["checksum"] == downloaded_file["checksum"]
    ):
        for _retry in range(0, retry_limit + 1):
            if _retry == retry_limit:
                display_message(msg_type="error", msg="Number of retries exceeded.")
                sys.exit(1)
            display_message(
                msg_type="note", msg="Retrying {}/{}".format(_retry + 1, retry_limit)
            )
            time.sleep(retry_sleep)
            download_single_file(
                path=path, file_location=file_location, protocol=protocol
            )
            downloaded_file = {
                "size": os.path.getsize(file_path),
                "checksum": get_file_checksum(file_path),
            }
            error = (
                DOWNLOAD_ERROR_PAGE["size"] == downloaded_file["size"]
                and DOWNLOAD_ERROR_PAGE["checksum"] == downloaded_file["checksum"]
            )
            if not error:
                return True


def show_download_progress(
    download_t=None, download_d=None, upload_t=None, upload_d=None
):
    """Show download progress of a file."""
    kb = 1024
    display_message(
        msg_type="progress",
        msg="Progress: {}/{} KiB ({}%)\r".format(
            str(int(download_d / kb)),
            str(int(download_t / kb)),
            str(int(download_d / download_t * 100) if download_t > 0 else 0),
        ),
    )
    sys.stdout.flush()


def download_single_file(path=None, file_location=None, protocol=None):
    """Download single file."""
    file_name = file_location.split("/")[-1]
    file_dest = path + "/" + file_name
    if protocol in ["http", "https"]:
        with open(file_dest, "wb") as f:
            display_message(
                msg_type="note",
                msg="File: ./{}/{}".format(
                    path,
                    file_name,
                ),
            )
            if pycurl_available:
                c = pycurl.Curl()
                c.setopt(c.URL, file_location)
                c.setopt(c.WRITEDATA, f)
                c.setopt(c.NOPROGRESS, False)
                c.setopt(c.XFERINFOFUNCTION, show_download_progress)
                c.perform()
                c.close()
            else:
                response = requests.get(file_location, stream=True)
                total_size = response.headers.get("content-length", 0)
                if total_size is None:
                    f.write(response.content)
                else:
                    downloaded = 0
                    kb = 1024
                    total_size = int(total_size)
                    for data in response.iter_content(chunk_size=kb):
                        downloaded += len(data)
                        f.write(data)
                        show_download_progress(
                            download_t=total_size, download_d=downloaded
                        )
        print()
    elif protocol == "xrootd":
        if not xrootd_available:
            display_message(
                msg_type="error",
                msg="xrootd is not installed on system. Please use the 'http' protocol instead.",
            )
            sys.exit(1)
        file_src = file_location.split("root://eospublic.cern.ch/")[-1]
        fs = XRootDPyFS("root://eospublic.cern.ch//")
        with open(file_dest, "wb") as dest, fs.open(file_src, "rb") as src:
            display_message(
                msg_type="note",
                msg="File: ./{}/{}".format(
                    path,
                    file_name,
                ),
            )
            src_data = src.read()
            dest.write(src_data)
    return


def get_download_files_by_name(names=None, file_locations=None):
    """Return the files filtered by file names.

    :param names: List of file names to be filtered
    :param file_locations: List of file locations
    :type names: list
    :type file_locations: list

    :return: List of file locations to be downloaded
    :rtype: list
    """
    download_file_locations = []
    for name in names:
        for file_location in file_locations:
            file_name = file_location.split("/")[-1]
            if file_name == name:
                download_file_locations.append(file_location)
    return download_file_locations


def get_download_files_by_regexp(regexp=None, file_locations=None, filtered_files=None):
    """Return the list of files filtered by a regular expression.

    :param regexp: Regexp string for filtering of file locations
    :param file_locations: List of file locations
    :param filtered_files: List of file locations filtered by previous filters(if any).
    :type regexp: str
    :type file_locations: list
    :type filtered_files: list

    :return: List of file locations to be downloaded
    :rtype: list
    """
    file_locations = filtered_files if filtered_files else file_locations
    download_file_locations = []
    for file_location in file_locations:
        file_name = file_location.split("/")[-1]
        if re.search(regexp, file_name):
            download_file_locations.append(file_location)
    return download_file_locations


def get_download_files_by_range(ranges=None, file_locations=None, filtered_files=None):
    """Return the list of files filtered by a range of files.

    :param ranges: List of ranges for filtering of files
    :param file_locations: List of file locations
    :param filtered_files: List of file locations filtered by previous filters(if any).
    :type ranges: list
    :type file_locations: list
    :type filtered_files: list

    :return: List of file locations to be downloaded
    :rtype: list
    """
    file_locations = filtered_files if filtered_files else file_locations
    download_file_locations = []
    for range in ranges:
        validate_range(range=range, count=len(file_locations))
        file_range = range.split("-")
        _range_file_locations = file_locations[
            int(file_range[0]) - 1 : int(file_range[-1])
        ]
        for file in _range_file_locations:
            download_file_locations.append(file)
    return download_file_locations
