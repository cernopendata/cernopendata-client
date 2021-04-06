# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2020, 2021 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client configuration."""


SERVER_HTTP_URI = "http://opendata.cern.ch"
"""Default CERN Open Data server to query over HTTP protocol."""

SERVER_HTTPS_URI = "https://opendata.cern.ch"
"""Default CERN Open Data server to query over HTTPS protocol."""

SERVER_ROOT_URI = "root://eospublic.cern.ch/"
"""Default CERN Open Data server to query over XRootD protocol."""

PRINTER_COLOUR_INFO = "green"
"""Default colour for info messages on terminal."""

PRINTER_COLOUR_NOTE = "blue"
"""Default colour for note messages on terminal."""

PRINTER_COLOUR_ERROR = "red"
"""Default colour for error messages on terminal."""

LIST_DIRECTORY_TIMEOUT = 60
"""Default timeout for list-directory command."""

DOWNLOAD_RETRY_LIMIT = 10
"""Default retries for getting a file from the server."""

DOWNLOAD_RETRY_SLEEP = 5
"""Sleep time in seconds before retrying downloads."""

DOWNLOAD_ERROR_PAGE = {"size": 3846, "checksum": "adler32:a82d5324"}
"""Error page info from the server."""

DOWNLOAD_ENGINE_PROTOCOL_HTTP_MAP = ["pycurl", "requests"]
"""Download engines compatible with HTTP protocol."""

DOWNLOAD_ENGINE_PROTOCOL_XROOTD_MAP = ["xrootd"]
"""Download engines compatible with xrootd protocol."""
