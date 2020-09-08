# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client command line tool."""

import click
import json
import os
import pycurl
import requests
import sys

from cernopendata_client.search import (
    get_files_list,
    get_recid,
    get_recid_api,
    get_record_as_json,
    verify_recid,
)
from cernopendata_client.tui import show_download_progress
from cernopendata_client.validator import (
    validate_recid,
    validate_server,
)
from cernopendata_client.version import __version__


@click.group()
def cernopendata_client():
    pass


@cernopendata_client.command()
def version():
    """Return cernopendata-client version."""
    print(__version__)


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier")
@click.option("--title", help="Title of the record")
@click.option(
    "--output-fields",
    is_flag=False,
    type=click.STRING,
    help="Comma-separated list of fields from the record "
    "that should be included in the output.",
)
@click.option(
    "--server",
    default="http://opendata.cern.ch",
    type=click.STRING,
    help="Which CERN Open Data server to query? [default=http://opendata.cern.ch]",
)
def get_metadata(server, recid, doi, title, output_fields):
    """Get metadata content of a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and return its metadata in the JSON format.

    \b
    Examples:
      $ cernopendata-client get-metadata --recid 1
      $ cernopendata-client get-metadata --recid 1 | jq -S '.metadata.title'
    """
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
    default="http",
    type=click.Choice(["http", "root"]),
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
    """Get a list of data file locations of a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and return the list of data file locations
    belonging to this record.

    \b
    Examples:
      $ cernopendata-client get-file-locations --recid 5500
      $ cernopendata-client get-file-locations --recid 5500 --protocol root
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    file_locations = get_files_list(server, record_json, protocol, expand)
    click.echo("\n".join(file_locations))


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier.")
@click.option("--title", help="Record title")
@click.option(
    "--protocol",
    default="http",
    type=click.Choice(["http", "root"]),
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
def download_files(server, recid, doi, title, protocol, expand):
    """Download data files belonging to a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and download data files belonging to this record.

    \b
    Examples:
      $ cernopendata-client download-files --recid 5500
    """

    if recid is not None:
        validate_recid(recid)
    if protocol == "root":
        click.secho(
            "Root protocol is not supported yet.",
            fg="red",
            err=True,
        )
        sys.exit(1)
    record_json = get_record_as_json(server, recid, doi, title)
    file_locations = get_files_list(server, record_json, protocol, expand)

    path = str(recid)
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
    total_files = len(file_locations)
    for file_location in file_locations:
        file_name = file_location.split("/")[-1]
        file_dest = path + "/" + file_name
        with open(file_dest, "wb") as f:
            print(
                "==> Downloading file {} of {}: ./{}/{}".format(
                    file_locations.index(file_location) + 1,
                    total_files,
                    path,
                    file_name,
                )
            )
            c = pycurl.Curl()
            c.setopt(c.URL, file_location)
            c.setopt(c.WRITEDATA, f)
            c.setopt(c.NOPROGRESS, False)
            c.setopt(c.XFERINFOFUNCTION, show_download_progress)
            c.perform()
            c.close()
    click.echo("\nDownload completed!")
