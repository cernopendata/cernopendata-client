# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

import json
import sys

import click
import requests
from requests import HTTPError

from cernopendata_client.search import (
    get_recid,
    verify_recid,
    get_recid_api,
    get_record_as_json,
)
from cernopendata_client.validator import (
    validate_recid,
    validate_server,
)


@click.group()
def cernopendata_client():
    pass


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier.")
@click.option("--title", help="Record title")
@click.option(
    "--output-fields",
    is_flag=False,
    type=click.STRING,
    help="Comma separated list of fields from the record "
    "that should be included in the output.",
)
@click.option(
    "--server",
    default="http://opendata.cern.ch",
    type=click.STRING,
    help="Which CERN Open Data server to query? [default=http://opendata.cern.ch]",
)
def get_record(server, recid, doi, title, output_fields):
    """Get records content by its recid, doi or title filtered."""
    # TODO: Add decorator to require one of (recid, doi or title)
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    if output_fields is not None:
        output_fields = [f.strip() for f in output_fields.split(",")]
    if output_fields and len(output_fields) > 0:
        try:
            output_json = {field: record_json[field] for field in output_fields}
        except KeyError:
            top_level_fields = ", ".join(field for field in record_json)
            click.secho(
                "Provided field is not top level field of this record."
                "\nFor this record top level fields are: {}"
                "\n\nFor deeper more complex queries you can use jq "
                "(see documentation for examples).".format(top_level_fields),
                fg="red",
                err=True,
            )
            sys.exit(1)
    else:
        output_json = record_json
    click.echo(json.dumps(output_json, indent=4))


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier.")
@click.option("--title", help="Record title")
@click.option(
    "--protocol",
    default="root",
    type=click.Choice(["root", "http"]),
    help="Protocol to be used in links.",
)
@click.option(
    "--expand/--no-expand", default=True, help="Expand file indexes? [default=yes]"
)
@click.option(
    "--server",
    default="http://opendata.cern.ch",
    type=click.STRING,
    help="Which CERN Open Data server to query? [default=http://opendata.cern.ch]",
)
def get_file_locations(server, recid, doi, title, protocol, expand):
    """Get a list of files belonging to a dataset."""
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    file_locations = [file["uri"] for file in record_json["metadata"]["files"]]
    if expand:
        # let's unwind file indexes
        file_locations_expanded = []
        for file in file_locations:
            if file.endswith("_file_index.txt"):
                url_file = file.replace("root://eospublic.cern.ch/", server)
                req = requests.get(url_file)
                for url_individual_file in req.text.split("\n"):
                    if url_individual_file:
                        file_locations_expanded.append(url_individual_file)
            elif file.endswith("_file_index.json"):
                pass
            else:
                file_locations_expanded.append(file)
        file_locations = file_locations_expanded

    if protocol == "http":
        file_locations = [
            f.replace("root://eospublic.cern.ch/", server) for f in file_locations
        ]
    click.echo("\n".join(file_locations))
