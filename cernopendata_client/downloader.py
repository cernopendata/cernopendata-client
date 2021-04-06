# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file downloading related utilities."""

from __future__ import print_function
import sys
import os
import re
import time

try:
    import requests

    requests_available = True
except ImportError:
    requests_available = False

try:
    import pycurl

    pycurl_available = True
except ImportError:
    pycurl_available = False

try:
    from XRootD import client as xrootdclient

    xrootd_available = True
except ImportError:
    xrootd_available = False


from .validator import validate_range
from .printer import display_message
from .verifier import get_file_checksum
from .config import (
    DOWNLOAD_ERROR_PAGE,
    DOWNLOAD_ENGINE_PROTOCOL_HTTP_MAP,
    DOWNLOAD_ENGINE_PROTOCOL_XROOTD_MAP,
    SERVER_ROOT_URI,
)


class DownloaderHttpRequests:
    """Downloader class for managing download related utilities with requests downloader engine."""

    def __init__(self, path, file_location, mode, file_size_offline):
        """Initialise class instance."""
        self.kb = 1024
        self.path = path
        self.mode = mode
        self.file_location = file_location
        self.file_name = self.file_location.split("/")[-1]
        self.file_dest = self.path + "/" + self.file_name
        self.file_size_offline = file_size_offline if file_size_offline else 0

    def show_download_progress(self, download_t=None, download_d=None):
        """Show download progress of a file."""
        display_message(
            msg_type="progress",
            msg="Progress: {}/{} KiB ({}%)\r".format(
                str(int(download_d / self.kb)),
                str(int(download_t / self.kb)),
                str(int(download_d / download_t * 100) if download_t > 0 else 0),
            ),
        )
        sys.stdout.flush()

    def file_downloader(self):
        """Download single file with requests."""
        headers = {}
        if self.file_size_offline:
            headers["Range"] = "bytes={}-".format(self.file_size_offline)
        response = requests.get(self.file_location, headers=headers, stream=True)
        total_size = int(response.headers.get("content-length", 0))
        with open(self.file_dest, self.mode) as f:
            display_message(
                msg_type="note",
                msg="File: ./{}/{}".format(
                    self.path,
                    self.file_name,
                ),
            )
            downloaded = self.file_size_offline
            total_size = total_size + self.file_size_offline
            for data in response.iter_content(chunk_size=1024):
                downloaded += len(data)
                try:
                    f.write(data)
                except Exception:
                    display_message(
                        msg_type="error",
                        msg="Download error occured. Please try again.",
                    )
                    sys.exit(1)
                self.show_download_progress(
                    download_t=total_size, download_d=downloaded
                )
                headers = {}


class DownloaderHttpPycurl:
    """Downloader class for managing download related utilities with pycurl downloader engine."""

    def __init__(self, path, file_location, mode, file_size_offline):
        """Initialise class instance."""
        self.kb = 1024
        self.path = path
        self.mode = mode
        self.file_location = file_location
        self.file_name = self.file_location.split("/")[-1]
        self.file_dest = self.path + "/" + self.file_name
        self.file_size_offline = file_size_offline if file_size_offline else 0

    def show_download_progress(
        self, download_t=None, download_d=None, upload_t=None, upload_d=None
    ):
        """Show download progress of a file."""
        download_t = download_t + self.file_size_offline
        download_d = download_d + self.file_size_offline
        display_message(
            msg_type="progress",
            msg="Progress: {}/{} KiB ({}%)\r".format(
                str(int(download_d / self.kb)),
                str(int(download_t / self.kb)),
                str(int(download_d / download_t * 100) if download_t > 0 else 0),
            ),
        )
        sys.stdout.flush()

    def file_downloader(self):
        """Download single file with pycurl."""
        c = pycurl.Curl()
        c.setopt(c.URL, self.file_location)
        if self.mode == "ab":
            c.setopt(c.RESUME_FROM, self.file_size_offline)
        with open(self.file_dest, self.mode) as f:
            display_message(
                msg_type="note",
                msg="File: ./{}/{}".format(
                    self.path,
                    self.file_name,
                ),
            )
            c.setopt(c.WRITEDATA, f)
            c.setopt(c.NOPROGRESS, False)
            c.setopt(c.XFERINFOFUNCTION, self.show_download_progress)
            try:
                c.perform()
            except Exception:
                display_message(
                    msg_type="error",
                    msg="Download error occured. Please try again.",
                )
                sys.exit(1)
            c.close()


class DownloaderXrootd:
    """Downloader class for managing download related utilities with xrootd downloader engine."""

    def __init__(self, path, file_location, mode):
        """Initialise class instance."""
        self.path = path
        self.mode = mode
        self.file_location = file_location
        self.file_name = self.file_location.split("/")[-1]
        self.file_dest = self.path + "/" + self.file_name
        self.file_src = self.file_location.split("root://eospublic.cern.ch/")[-1]

    def show_download_progress(self):
        """Show download progress of a file."""
        return

    def file_downloader(self):
        """Download single file with XRootD."""
        try:
            display_message(
                msg_type="note",
                msg="File: ./{}/{}".format(
                    self.path,
                    self.file_name,
                ),
            )
            process = xrootdclient.CopyProcess()
            process.add_job(
                SERVER_ROOT_URI + self.file_src, os.getcwd() + os.sep + self.file_dest
            )
            process.prepare()
            process.run()
        except Exception:
            display_message(
                msg_type="error", msg="Download error occured. Please try again."
            )


def check_error(
    path=None, file_location=None, protocol=None, retry_limit=None, retry_sleep=None
):
    """Return True if the file size and checksum does not matches with download error page.

    :param path: Directory where file is downloaded
    :param file_location: Remote location of a file
    :param protocol: Protocol to be used for downloading a file
    :param retry_limit: Number of retries to be made for downloading a file.
    :param retry_sleep: Time of sleep before every retry.
    :type path: str
    :type file_location: str
    :type protocol: str
    :type retry_limit: int
    :type retry_sleep: int

    :return: True if the file size and checksum does not matches with download error page.
    :rtype: Boolean
    """
    file_name = file_location.split("/")[-1]
    file_dest = path + "/" + file_name
    downloaded_file = {
        "size": os.path.getsize(file_dest),
        "checksum": get_file_checksum(file_dest),
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
                "size": os.path.getsize(file_dest),
                "checksum": get_file_checksum(file_dest),
            }
            error = (
                DOWNLOAD_ERROR_PAGE["size"] == downloaded_file["size"]
                and DOWNLOAD_ERROR_PAGE["checksum"] == downloaded_file["checksum"]
            )
            if not error:
                return True


def downloader_file_checker(file_location, file_dest):
    """Return False if file is not present in the directory else True.

    :param file_location: Remote location of a file
    :param file_dest: Expected local destination path of a file
    :type file_location: str
    :type file_dest: str

    :return: False if file is not present in the directory else True
    :rtype: Boolean
    """
    try:
        response = requests.head(file_location)
        file_size_online = int(response.headers.get("content-length", 0))
    except Exception:
        display_message(
            msg_type="error",
            msg="Download error occured. Please try again.",
        )
    if os.path.isfile(file_dest):
        file_size_offline = os.path.getsize(file_dest)
        return file_size_online != file_size_offline
    return False


def download_single_file(
    path=None, file_location=None, protocol=None, download_engine=None
):
    """Download a single file.

    :param path: Directory where file is downloaded
    :param file_location: Remote location of a file
    :param protocol: Protocol to be used for downloading a file
    :param download_engine: Library to be used in downloading files
    :type path: str
    :type file_location: str
    :type protocol: str
    :type download_engine: str

    :return: None
    :rtype: None
    """
    file_name = file_location.split("/")[-1]
    file_dest = path + "/" + file_name
    download_engine_map = {
        "requests": requests_available,
        "pycurl": pycurl_available,
        "xrootd": xrootd_available,
    }
    if download_engine:
        if not download_engine_map.get(download_engine):
            display_message(
                msg_type="error",
                msg="{} is not installed on system. Please install it.".format(
                    download_engine
                ),
            )
            sys.exit(1)
    if protocol in ["http", "https"]:
        if download_engine not in DOWNLOAD_ENGINE_PROTOCOL_HTTP_MAP:
            display_message(
                msg_type="error",
                msg="{} is not compatible with {} protocol. Please use requests or pycurl download engine.".format(
                    download_engine,
                    protocol,
                ),
            )
            sys.exit(1)
        file_download_incomplete = downloader_file_checker(file_location, file_dest)
        if file_download_incomplete:
            file_size_offline = os.path.getsize(file_dest)
            mode = "ab"
            display_message(
                msg_type="note",
                msg="File {} is incomplete. Resuming download.".format(
                    file_name,
                ),
            )
        else:
            file_size_offline = None
            mode = "wb"
        if download_engine == "requests":
            downloader = DownloaderHttpRequests(
                path, file_location, mode, file_size_offline
            )
            downloader.file_downloader()
        elif download_engine == "pycurl":
            downloader = DownloaderHttpPycurl(
                path, file_location, mode, file_size_offline
            )
            downloader.file_downloader()
        print()
    elif protocol == "xrootd":
        if download_engine not in DOWNLOAD_ENGINE_PROTOCOL_XROOTD_MAP:
            display_message(
                msg_type="error",
                msg="{} is not compatible with {} protocol. Please use xrootd engine.".format(
                    download_engine,
                    protocol,
                ),
            )
            sys.exit(1)
        mode = "wb"
        downloader = DownloaderXrootd(path, file_location, mode)
        downloader.file_downloader()
    return


def get_download_files_by_name(names=None, file_locations=None):
    """Return the files filtered by file names.

    :param names: List of file names to be filtered
    :param file_locations: List of remote file locations
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
    :param file_locations: List of remote file locations
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
    :param file_locations: List of remote file locations
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
