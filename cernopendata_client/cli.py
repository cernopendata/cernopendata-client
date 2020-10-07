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
import requests
import sys
import re

from .searcher import (
    get_file_info_remote,
    get_files_list,
    get_recid,
    get_recid_api,
    get_record_as_json,
    verify_recid,
)
from .downloader import (
    download_single_file,
    get_download_files_by_name,
    get_download_files_by_range,
    get_download_files_by_regexp,
)
from .validator import (
    validate_range,
    validate_recid,
    validate_server,
)
from .verifier import get_file_info_local
from .utils import parse_parameters

from .version import __version__


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
    "--output-value",
    is_flag=False,
    type=click.STRING,
    help="Output only value of a desired metadata field.",
)
@click.option(
    "--server",
    default="http://opendata.cern.ch",
    type=click.STRING,
    help="Which CERN Open Data server to query? [default=http://opendata.cern.ch]",
)
def get_metadata(server, recid, doi, title, output_value):
    """Get metadata content of a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and return its metadata in the JSON format.

    \b
    Examples:
      $ cernopendata-client get-metadata --recid 1
      $ cernopendata-client get-metadata --recid 1 --output-value system_details.global_tag
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    output_json = record_json["metadata"]
    if not output_value:
        click.echo(json.dumps(output_json, indent=4))
    else:
        fields = output_value.split(".")
        for field in fields:
            try:
                output_json = output_json[field]
            except (KeyError, TypeError):
                click.secho(
                    "Field '{}' is not present in metadata".format(field),
                    fg="red",
                    err=True,
                )
                sys.exit(1)
        if not output_json:
            click.secho(
                "Field '{}' is not present in metadata.".format(fields),
                fg="red",
                err=True,
            )
            sys.exit(1)
        if type(output_json) is dict or type(output_json) is list:
            click.echo(json.dumps(output_json, indent=4))
        else:  # print strings or numbers more simply
            click.echo(output_json)


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
@click.option(
    "--dry-run/--no-dry-run",
    "dryrun",
    default=False,
    help="Get the list of data file locations to be downloaded.",
)
@click.option(
    "--filter-name",
    "names",
    multiple=True,
    type=click.STRING,
    help="Download files matching exactly the file name",
)
@click.option(
    "--filter-regexp",
    "regexp",
    type=click.STRING,
    help="Download files matching the regular expression",
)
@click.option(
    "--filter-range",
    "ranges",
    multiple=True,
    type=click.STRING,
    help="Download files from a specified list range (i-j)",
)
def download_files(
    server, recid, doi, title, protocol, expand, names, regexp, ranges, dryrun
):
    """Download data files belonging to a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and download data files belonging to this record.

    \b
    Examples:
      $ cernopendata-client download-files --recid 5500
      $ cernopendata-client download-files --recid 5500 --filter-name name=BuildFile.xml
      $ cernopendata-client download-files --recid 5500 --filter-name name=BuildFile.xml,name=List_indexfile.txt
      $ cernopendata-client download-files --recid 5500 --filter-regexp py$
      $ cernopendata-client download-files --recid 5500 --filter-range range=1-4
      $ cernopendata-client download-files --recid 5500 --filter-range range=1-2,range=5-7
      $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range range=1-2
      $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range range=1-2,range=3-4
    """

    if recid is not None:
        validate_recid(recid)
    if protocol == "root" and not dryrun:
        click.secho(
            "Root protocol is not supported yet.",
            fg="red",
            err=True,
        )
        sys.exit(1)
    record_json = get_record_as_json(server, recid, doi, title)
    file_locations = get_files_list(server, record_json, protocol, expand)
    download_file_locations = []

    if names:
        parsed_name_filters = parse_parameters(names)
        dload_file_location_name = get_download_files_by_name(
            names=parsed_name_filters, file_locations=file_locations
        )
        download_file_locations = dload_file_location_name
    if regexp:
        dload_file_location_regexp = get_download_files_by_regexp(
            regexp=regexp,
            file_locations=file_locations,
            dload=download_file_locations if names else None,
        )
        download_file_locations = dload_file_location_regexp
    if ranges:
        parsed_range_filters = parse_parameters(ranges)
        dload_file_location_range = get_download_files_by_range(
            ranges=parsed_range_filters,
            file_locations=file_locations,
            dload=download_file_locations if names or regexp else None,
        )
        download_file_locations = dload_file_location_range

    if names or regexp or ranges:
        if not download_file_locations:
            click.echo("\nNo files matching the filters")
            sys.exit(1)
    else:
        download_file_locations = file_locations

    if dryrun:
        click.echo("\n".join(download_file_locations))
        sys.exit(0)

    total_files = len(download_file_locations)
    path = str(recid)
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory {} failed".format(path))
    for file_location in download_file_locations:
        print(
            "==> Downloading file {} of {}".format(
                download_file_locations.index(file_location) + 1, total_files
            )
        )
        download_single_file(path=path, file_location=file_location)

    click.echo("==> Success!")


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option(
    "--server",
    default="http://opendata.cern.ch",
    type=click.STRING,
    help="Which CERN Open Data server to query? [default=http://opendata.cern.ch]",
)
def verify_files(server, recid):
    """Verify downloaded data file integrity.

    Select a CERN Open Data bibliographic record by a record ID and
    verify integrity of downloaded data files belonging to this
    record.

    \b
    Examples:
      $ cernopendata-client verify-files --recid 5500
    """

    # Validate parameters
    validate_recid(recid)

    # Get remote file information
    file_info_remote = get_file_info_remote(recid)

    # Get local file information
    file_info_local = get_file_info_local(recid)
    if not file_info_local:
        print(
            "ERROR: No local files found for record {}. Perhaps run `download-files` first? Exiting.".format(
                recid
            )
        )
        sys.exit(1)

    # Verify number of files
    print("==> Verifying number of files for record {}... ".format(recid))
    print(
        "  -> expected {}, found {}".format(len(file_info_remote), len(file_info_local))
    )
    if len(file_info_remote) != len(file_info_local):
        print("ERROR: File count does not match.")
        sys.exit(1)

    # Verify size and checksum of each file
    for afile_info_remote in file_info_remote:
        afile_name = afile_info_remote["name"]
        afile_size = afile_info_remote["size"]
        afile_checksum = afile_info_remote["checksum"]
        bfile_size = 0
        bfile_checksum = ""
        for bfile_info_local in file_info_local:
            if bfile_info_local["name"] == afile_name:
                bfile_size = bfile_info_local["size"]
                bfile_checksum = bfile_info_local["checksum"]
                break
        print("==> Verifying file {}... ".format(afile_name))
        print("  -> expected size {}, found {}".format(afile_size, bfile_size))
        if afile_size != bfile_size:
            print("ERROR: File size does not match.")
            sys.exit(1)
        print(
            "  -> expected checksum {}, found {}".format(afile_checksum, bfile_checksum)
        )
        if afile_checksum != bfile_checksum:
            print("ERROR: File checksum does not match.")
            sys.exit(1)

    # Success!
    print("==> Success!")
