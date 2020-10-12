# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client utility functions."""

import click


def parse_parameters(filter_input):
    """Return parsed filter parameters.

    :param filter_input: Tuple of filters input
    :type filter_input: tuple

    :return: List of filters separated by commas
    :rtype: list
    """
    try:
        filters = " ".join(filter_input).split(",")
        return filters
    except Exception:
        raise click.BadParameter("Wrong input format \n")
