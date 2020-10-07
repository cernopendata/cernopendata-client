# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client utility functions."""

import shlex
import click


def parse_parameters(filter_input):
    """Return parsed filter parameters."""
    try:
        parsed_filters = []
        filters = " ".join(filter_input).replace(",", " ")
        for item in shlex.split(filters):
            if "=" in item:
                filter_item = {
                    "filter": item.split("=")[0].lower(),
                    "value": item.split("=")[1],
                }
            else:
                raise click.BadParameter("Wrong filter format \n")
            parsed_filters.append(filter_item)
        return parsed_filters
    except:
        raise click.BadParameter("Wrong input format \n")
