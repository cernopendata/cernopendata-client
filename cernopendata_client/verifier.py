# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file verifier related utilities."""

import os
import zlib


def get_file_size(afile):
    """Return the size of a file."""
    return os.path.getsize(afile)


def get_file_checksum(afile):
    """Return the ADLER32 checksum of a file."""
    return "adler32:" + hex(zlib.adler32(open(afile, "rb").read(), 1) & 0xFFFFFFFF)[2:]


def get_file_info_local(recid):
    """Return local file information list for given record.

    Returns a list of dictionaries containing (checksum, name, size)
    for each file found downloaded in output directory matching recid.
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
