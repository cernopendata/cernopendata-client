# -*- coding: utf-8 -*-
#
# This file is part of REANA.
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client output print configuration."""

import click

from .config import PRINTER_COLOUR_ERROR, PRINTER_COLOUR_INFO, PRINTER_COLOUR_NOTE


def display_message(msg_type=None, msg=None):
    """Display message in a similar style as run_command().

    :param msg_type: Type of message (info/note/error)
    :param msg: message to display
    :type msg_type: str
    :type msg: str
    """
    msg_color_map = {
        "info": PRINTER_COLOUR_INFO,
        "note": PRINTER_COLOUR_NOTE,
        "progress": PRINTER_COLOUR_NOTE,
        "error": PRINTER_COLOUR_ERROR,
    }
    msg_color = msg_color_map.get(msg_type, "")

    if msg_type == "info":
        click.secho("==> ", bold=True, nl=False, fg="{}".format(msg_color))
        click.secho("{}".format(msg), bold=True, nl=True)
    elif msg_type == "note":
        click.secho("  -> ", bold=False, nl=False, fg="{}".format(msg_color))
        click.secho("{}".format(msg), bold=False, nl=True)
    elif msg_type == "progress":
        click.secho("  -> ", bold=False, nl=False, fg="{}".format(msg_color))
        click.secho("{}".format(msg), bold=False, nl=False)
    elif msg_type == "error":
        click.secho(
            "==> {}: ".format(msg_type.upper()),
            bold=True,
            nl=False,
            fg="{}".format(msg_color),
        )
        click.secho("{}".format(msg), bold=False, nl=True)
    else:
        click.secho("{}".format(msg), nl=True)
