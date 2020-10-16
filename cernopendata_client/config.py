# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client configuration."""


SERVER_HTTP_URI = "http://opendata.cern.ch"
"""Default CERN Open Data server to query over HTTP protocol."""

SERVER_ROOT_URI = "root://eospublic.cern.ch/"
"""Default CERN Open Data server to query over XRootD protocol."""

PRINTER_COLOUR_INFO = "bright_yellow"
"""Default Color for info message on terminal"""

PRINTER_COLOUR_ERROR = "bright_red"
"""Default Color for error message on terminal"""

PRINTER_COLOUR_SUCCESS = "bright_green"
"""Default Color for success message on terminal"""
