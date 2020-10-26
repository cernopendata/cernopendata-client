# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client output print configuration."""

import click

from .config import PRINTER_COLOUR_ERROR, PRINTER_COLOUR_INFO, PRINTER_COLOUR_SUCCESS


def display_message(prefix=None, msg_type=None, msg=None):
    """Display message in a similar style as run_command().

    :param prefix: prefix to be added in output (==> / ->)
    :param msg_type: Type of message - Error/Progress/Success
    :param msg: message to display
    :type prefix: str
    :type msg_type: str
    :type msg: str
    """
    msg_color_map = {
        "info": PRINTER_COLOUR_INFO,
        "error": PRINTER_COLOUR_ERROR,
        "success": PRINTER_COLOUR_SUCCESS,
    }
    msg_color = msg_color_map.get(msg_type, None)

    if prefix == "double":
        if msg_color:
            click.secho("==> ", bold=True, nl=False, fg="{}".format(msg_color))
        if msg_type == "error":
            click.secho(
                "{}: ".format(msg_type.upper()),
                bold=True,
                nl=False,
                fg=PRINTER_COLOUR_ERROR,
            )
    elif prefix == "single":
        click.secho("  -> ", bold=False, nl=False)

    if msg_color:
        click.secho("{}".format(msg), bold=True, nl=True, fg="{}".format(msg_color))
    else:
        click.secho("{}".format(msg), bold=False, nl=True)
