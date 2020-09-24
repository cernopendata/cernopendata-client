# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

from sys import stderr as STREAM
import re
import pycurl


def show_download_progress(download_t, download_d, upload_t, upload_d):
    """Show download progress of a file"""
    kb = 1024
    STREAM.write(
        "  -> Progress: {}/{} kiB ({}%)\r".format(
            str(int(download_d / kb)),
            str(int(download_t / kb)),
            str(int(download_d / download_t * 100) if download_t > 0 else 0),
        )
    )
    STREAM.flush()


def download_single_file(path=None, file_location=None):
    """Download single file"""
    file_name = file_location.split("/")[-1]
    file_dest = path + "/" + file_name
    with open(file_dest, "wb") as f:
        print(
            "  -> File: ./{}/{}".format(
                path,
                file_name,
            )
        )
        c = pycurl.Curl()
        c.setopt(c.URL, file_location)
        c.setopt(c.WRITEDATA, f)
        c.setopt(c.NOPROGRESS, False)
        c.setopt(c.XFERINFOFUNCTION, show_download_progress)
        c.perform()
        c.close()
    print()
    return


def get_download_files_by_name(name=None, file_locations=None):
    """Returns the file filtered by the name"""
    for file_location in file_locations:
        file_name = file_location.split("/")[-1]
        if file_name == name:
            return [file_location]


def get_download_files_by_regexp(regexp=None, file_locations=None, **kwargs):
    """
    dload kwarg - List of file locations filtered by previous filters(if any)
    Returns the list of files filtered by a regular expression
    """
    _file_locations = kwargs.get("dload", None)
    file_locations = _file_locations if _file_locations else file_locations
    download_file_locations = []
    for file_location in file_locations:
        file_name = file_location.split("/")[-1]
        if re.search(regexp, file_name):
            download_file_locations.append(file_location)
    return download_file_locations


def get_download_files_by_range(range=None, file_locations=None, **kwargs):
    """
    dload kwarg - List of file locations filtered by previous filters(if any)
    Returns the list of files filtered by a range of files
    """
    _file_locations = kwargs.get("dload", None)
    file_locations = _file_locations if _file_locations else file_locations
    file_range = range.split("-")
    download_file_locations = file_locations[
        int(file_range[0]) - 1 : int(file_range[-1])
    ]
    return download_file_locations
