# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2025, 2026 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file verifier related utilities."""

import os
import sys
import zlib

from .printer import display_message

CHECKSUM_CHUNK_SIZE = 1024 * 1024


def get_file_size(afile):
    """Return the size of a file.

    :param afile: file name
    :type afile: str

    :return: Size of file
    :rtype: int
    """
    return os.path.getsize(afile)


def get_file_checksum(afile):
    """Return the ADLER32 checksum of a file.

    :param afile: file name
    :type afile: str

    :return: Adler32 checksum of file
    :rtype: str
    """
    checksum = 1
    with open(afile, "rb") as f:
        while True:
            chunk = f.read(CHECKSUM_CHUNK_SIZE)
            if not chunk:
                break
            checksum = zlib.adler32(chunk, checksum)
    return "adler32:{:08x}".format(checksum & 0xFFFFFFFF)


def get_local_file_paths(adir):
    """Return all regular files below a directory in deterministic order."""
    local_file_paths = []
    if not os.path.isdir(adir):
        return local_file_paths
    for root, directories, files in os.walk(adir):
        directories.sort()
        for afile in sorted(files):
            local_file_paths.append(os.path.join(root, afile))
    return local_file_paths


def get_file_info_local(recid):
    """Return the local file information list for given record.

    :param recid: Record ID
    :type recid: str

    :return: Returns a list of dictionaries containing (checksum, name, size)
    for each file found downloaded in output directory matching recid.
    :rtype: list
    """
    file_info_local = []

    adir = str(recid)
    if not os.path.exists(adir):
        return file_info_local

    for afile in os.listdir(adir):
        file_info_local.append(
            {
                "name": afile,
                "size": get_file_size(adir + os.path.sep + afile),
                "checksum": get_file_checksum(adir + os.path.sep + afile),
            }
        )

    return file_info_local


def verify_downloaded_file(
    afile,
    expected_size=None,
    expected_checksum=None,
    verify_checksum=True,
):
    """Verify one exact local path against the supplied record metadata."""
    display_message(
        msg_type="info",
        msg="Verifying file {}... ".format(afile),
    )
    if not os.path.isfile(afile):
        display_message(
            msg_type="error",
            msg="Downloaded file is missing: {}.".format(afile),
        )
        sys.exit(1)

    actual_size = get_file_size(afile)
    if expected_size is not None:
        display_message(
            msg_type="note",
            msg="Expected size {}, found {}".format(expected_size, actual_size),
        )
        if expected_size != actual_size:
            size_failure = "incomplete" if actual_size < expected_size else "oversized"
            display_message(
                msg_type="error",
                msg="File size does not match; the file is {}.".format(size_failure),
            )
            sys.exit(1)

    if verify_checksum and expected_checksum:
        actual_checksum = get_file_checksum(afile)
        display_message(
            msg_type="note",
            msg="Expected checksum {}, found {}".format(
                expected_checksum, actual_checksum
            ),
        )
        if expected_checksum != actual_checksum:
            display_message(
                msg_type="error",
                msg="File checksum does not match.",
            )
            sys.exit(1)
    return True


def verify_file_info(file_info_local, file_info_remote):
    """Return True if local file info matches with the remote file info.

    :param file_info_local: List of files in local directory
    :param file_info_remote: List of files in remote server
    :type file_info_local: list
    :type file_info_remote: list

    :return: Bool if local file info matches with the remote file info.
    :rtype: Bool
    """
    for afile_info_remote in file_info_remote:
        afile_name = afile_info_remote["name"]
        afile_size = afile_info_remote["size"]
        afile_checksum = afile_info_remote["checksum"]
        bfile_size = 0
        bfile_checksum = ""
        for bfile_info_local in file_info_local:
            if bfile_info_local["name"] == afile_name:
                bfile_size = bfile_info_local["size"]
                bfile_checksum = bfile_info_local["checksum"]
                break
        display_message(
            msg_type="info",
            msg="Verifying file {}... ".format(afile_name),
        )
        display_message(
            msg_type="note",
            msg="Expected size {}, found {}".format(afile_size, bfile_size),
        )
        if afile_size != bfile_size:
            display_message(
                msg_type="error",
                msg="File size does not match.",
            )
            sys.exit(1)
        display_message(
            msg_type="note",
            msg="Expected checksum {}, found {}".format(afile_checksum, bfile_checksum),
        )
        if afile_checksum != bfile_checksum:
            display_message(msg_type="error", msg="File checksum does not match.")
            sys.exit(1)
    return True
