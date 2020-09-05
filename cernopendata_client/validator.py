# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

import click


def validate_recid(recid=None):
    """Validate record ID.

    Returns True if OK, raises click.BadParameter exception otherwise.
    """
    if recid <= 0:
        raise click.BadParameter(
            "Recid should be a positive integer",
            param_hint=["--recid"],
        )
    return True


def validate_server(server=None):
    """Validate server URL.

    Returns True if OK, raises click.BadParameter exception otherwise.
    """
    if not server.startswith("http://"):
        raise click.BadParameter(
            "Server should be a valid URL",
            param_hint=["--server"],
        )
    return True
