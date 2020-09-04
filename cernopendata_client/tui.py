# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

from sys import stderr as STREAM


def show_download_progress(download_t, download_d, upload_t, upload_d):
    """Show download progress of a file"""
    kb = 1024
    STREAM.write(
        "Downloading: {}/{} kiB ({}%)\r".format(
            str(int(download_d / kb)),
            str(int(download_t / kb)),
            str(int(download_d / download_t * 100) if download_t > 0 else 0),
        )
    )
    STREAM.flush()
