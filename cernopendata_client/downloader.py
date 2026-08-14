# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2021, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file downloading related utilities."""

from __future__ import print_function
from dataclasses import dataclass
from typing import Optional

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


@dataclass(frozen=True)
class DownloadItem:
    """Describe one selected download and its exact local destination."""

    file_location: str
    expected_size: Optional[int]
    expected_checksum: Optional[str]
    destination_directory: str
    destination_path: str
    is_file_index: bool = False


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
        status = process.prepare()
        if status.ok:
            status, _ = process.run()
        if not status.ok:
            display_message(
                msg_type="error",
                msg="Download error: {}".format(status.message.strip()),
            )
            sys.exit(1)


def check_error(
    path=None,
    file_location=None,
    protocol=None,
    retry_limit=None,
    retry_sleep=None,
    download_engine=None,
):
    """Return True if the file size and checksum does not matches with download error page.

    :param path: Directory where file is downloaded
    :param file_location: Remote location of a file
    :param protocol: Protocol to be used for downloading a file
    :param retry_limit: Number of retries to be made for downloading a file.
    :param retry_sleep: Time of sleep before every retry.
    :param download_engine: Library to be used in downloading files.
    :type path: str
    :type file_location: str
    :type protocol: str
    :type retry_limit: int
    :type retry_sleep: int
    :type download_engine: str

    :return: True if the file size and checksum does not matches with download error page.
    :rtype: Boolean
    """
    file_name = file_location.split("/")[-1]
    file_dest = os.path.join(path, file_name)
    if not _is_download_error_page(file_dest):
        return True

    for _retry in range(0, retry_limit or 0):
        display_message(
            msg_type="note", msg="Retrying {}/{}".format(_retry + 1, retry_limit)
        )
        time.sleep(retry_sleep)
        download_single_file(
            path=path,
            file_location=file_location,
            protocol=protocol,
            download_engine=download_engine,
        )
        if not _is_download_error_page(file_dest):
            return True

    display_message(msg_type="error", msg="Number of retries exceeded.")
    sys.exit(1)


def _is_download_error_page(file_dest):
    """Return whether a destination contains the known download error page."""
    if not os.path.isfile(file_dest):
        return False
    if os.path.getsize(file_dest) != DOWNLOAD_ERROR_PAGE["size"]:
        return False
    return get_file_checksum(file_dest) == DOWNLOAD_ERROR_PAGE["checksum"]


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
    path=None,
    file_location=None,
    protocol=None,
    download_engine=None,
    expected_size=None,
):
    """Download a single file.

    :param path: Directory where file is downloaded
    :param file_location: Remote location of a file
    :param protocol: Protocol to be used for downloading a file
    :param download_engine: Library to be used in downloading files
    :param expected_size: Final file size from record metadata, if applicable
    :type path: str
    :type file_location: str
    :type protocol: str
    :type download_engine: str
    :type expected_size: int

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
        file_download_incomplete = False
        if os.path.isfile(file_dest) and expected_size is not None:
            file_download_incomplete = os.path.getsize(file_dest) < expected_size
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


def get_file_subdirectories(file_locations):
    """Return a mapping of file locations to subdirectory paths for disambiguation.

    When multiple files share the same file name, compute subdirectory paths
    by stripping the longest common directory prefix from the URL paths.
    This preserves the original directory structure relative to the common root.

    :param file_locations: List of remote file locations (URLs)
    :type file_locations: list

    :return: Dictionary mapping each file location to its subdirectory (empty
        string if no subdirectory is needed)
    :rtype: dict
    """
    from collections import Counter

    file_names = [loc.split("/")[-1] for loc in file_locations]
    file_name_counts = Counter(file_names)
    has_duplicates = any(count > 1 for count in file_name_counts.values())

    if not has_duplicates:
        return {loc: "" for loc in file_locations}

    # Split each URL into directory components (excluding the filename)
    dir_parts_list = [loc.split("/")[:-1] for loc in file_locations]
    # Find the longest common prefix of all directory paths
    common_prefix_len = 0
    if dir_parts_list:
        min_len = min(len(parts) for parts in dir_parts_list)
        for i in range(min_len):
            if len(set(parts[i] for parts in dir_parts_list)) == 1:
                common_prefix_len = i + 1
            else:
                break
    # Build subdirectory for each file by stripping the common prefix
    result = {}
    for loc, dir_parts in zip(file_locations, dir_parts_list):
        subdir = "/".join(dir_parts[common_prefix_len:])
        result[loc] = subdir
    return result


def get_download_path(base_path, file_location, file_subdirs):
    """Return download path for a file, creating subdirectories if needed.

    :param base_path: Base directory for downloads (e.g. record ID)
    :param file_location: Remote file location URL
    :param file_subdirs: Mapping from file locations to subdirectory paths
    :type base_path: str
    :type file_location: str
    :type file_subdirs: dict

    :return: Local directory path where the file should be saved
    :rtype: str
    """
    subdir = file_subdirs[file_location]
    if subdir:
        path = os.path.join(base_path, subdir)
        os.makedirs(path, exist_ok=True)
        return path
    return base_path


def get_download_items(base_path, file_entries, layout_entries=None):
    """Return selected downloads with exact destinations and metadata.

    :param base_path: Base directory for downloads
    :param file_entries: Selected file metadata entries
    :param layout_entries: All entries used to disambiguate destination paths
    :type base_path: str
    :type file_entries: list
    :type layout_entries: list

    :return: Selected downloads with exact destinations and metadata
    :rtype: list
    """
    layout_entries = layout_entries if layout_entries is not None else file_entries
    file_locations = [entry.uri for entry in layout_entries]
    file_subdirs = get_file_subdirectories(file_locations)
    download_items = []
    for entry in file_entries:
        subdir = file_subdirs[entry.uri]
        destination_directory = os.path.join(base_path, subdir) if subdir else base_path
        destination_path = os.path.join(
            destination_directory, entry.uri.rsplit("/", 1)[-1]
        )
        download_items.append(
            DownloadItem(
                file_location=entry.uri,
                expected_size=None if entry.is_file_index else entry.size,
                expected_checksum=(
                    None if entry.is_file_index else entry.checksum or None
                ),
                destination_directory=destination_directory,
                destination_path=destination_path,
                is_file_index=entry.is_file_index,
            )
        )
    return download_items


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
