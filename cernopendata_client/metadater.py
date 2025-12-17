# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2023, 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client file metadater related utilities."""

import json
import sys
from collections import Counter

from .printer import display_message


def handle_error_message(field):
    # noqa: D301
    """Handle error message.

    :param field: Name of the field to access

    :type field: str

    :return: None
    """
    display_message(
        msg_type="error",
        msg="Field '{}' is not present in metadata".format(field),
    )
    sys.exit(1)


def filter_matching_output(matching_objects, output_field, output_json):
    # noqa: D301
    """Filter matching objects based on specified criteria.

    :param possible: Dictionary containing matching objects
    :param output_field: Name of the array containing objects to access
    :param output_json: JSON containing metadata objects

    :type possible: dict
    :type field: str
    :type output_json: list or dict

    :return: None
    """
    index_frequency = Counter(
        [int(item.split("_")[1]) for item in matching_objects.keys()]
    )

    output_object_index, count = index_frequency.most_common(1)[0]
    output_object = output_json[output_object_index]
    if count == 1:
        for object in matching_objects.values():
            if output_field in object:
                display_message(msg=object[output_field])
            else:
                display_message(msg=json.dumps(object, indent=4))
    else:
        if output_field in output_object:
            display_message(msg=output_object[output_field])
        else:
            display_message(msg=json.dumps(output_object, indent=4))


def filter_metadata(output_field, filters, output_json):
    # noqa: D301
    """Filter metadata objects based on specified criteria.

    :param output_field: Name of the array containing objects to access
    :param filters: Argument of the --filter option in the format some_field_name=some_value
    :param output_json: JSON containing metadata objects

    :type field: str
    :type filters: str
    :type output_json: list or dict

    :return: None
    """
    matching_objects = {}
    for filter in filters:
        no_objects_found = True
        wrong_field = True

        filter_fields = filter.split("=")
        if len(filter_fields) != 2:
            display_message(
                msg_type="error",
                msg="Invalid filter format. Use --filter some_field_name=some_value",
            )
            sys.exit(1)
        filterField_name, filterField_value = filter_fields
        filterField_names = filterField_name.split(".")
        for index, object in enumerate(output_json):
            if object == "$schema":
                handle_error_message(output_field)
            if filterField_name in object:
                wrong_field = False
                if filterField_value == object[filterField_names[-1]]:
                    matching_objects[f"{filterField_names[-1]}_{index}"] = object
                    no_objects_found = False
        if no_objects_found and not wrong_field:
            display_message(
                msg_type="error",
                msg="No objects found with {}={}".format(
                    filterField_names[-1], filterField_value
                ),
            )
            sys.exit(1)
        elif wrong_field:
            handle_error_message(filterField_names[-1])
    if matching_objects:
        filter_matching_output(matching_objects, output_field, output_json)
