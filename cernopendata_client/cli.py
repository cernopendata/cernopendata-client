# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020, 2021, 2023, 2025, 2026 CERN.
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
    get_file_entries,
    get_files_list,
    get_recid,
    get_recid_api,
    get_record_as_json,
    verify_recid,
)
from .downloader import (
    check_error,
    download_single_file,
    get_download_files_by_name,
    get_download_files_by_range,
    get_download_files_by_regexp,
    get_download_items,
)
from .validator import (
    validate_range,
    validate_recid,
    validate_server,
    validate_directory,
    validate_retry_limit,
    validate_retry_sleep,
)
from .walker import get_list_directory
from .verifier import get_local_file_paths, verify_downloaded_file
from .metadater import filter_metadata, handle_error_message
from .config import (
    SERVER_HTTP_URI,
    LIST_DIRECTORY_TIMEOUT,
    DOWNLOAD_RETRY_LIMIT,
    DOWNLOAD_RETRY_SLEEP,
)
from .utils import parse_parameters
from .printer import display_message

from .version import __version__


@click.group()
def cernopendata_client():
    """Command-line client for interacting with CERN Open Data portal."""
    pass


@cernopendata_client.command()
def version():
    """Return cernopendata-client version.

    Examples: \n
    \t $ cernopendata-client version
    """
    display_message(msg=__version__)


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID (exact match)")
@click.option("--doi", help="Digital Object Identifier (exact match)")
@click.option("--title", help="Record title (exact match, no wildcards)")
@click.option(
    "--output-value",
    is_flag=False,
    type=click.STRING,
    help="Output value of only desired metadata field [example=title]",
)
@click.option(
    "--server",
    default=SERVER_HTTP_URI,
    type=click.STRING,
    help="Which CERN Open Data server to query? [default={}]".format(SERVER_HTTP_URI),
)
@click.option(
    "--filter",
    "filters",
    multiple=True,
    help="Filter only certain output values matching filtering criteria. [Use --filter some_field_name=some_value]",
)
def get_metadata(server, recid, doi, title, output_value, filters):
    # noqa: D301
    """Get metadata content of a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and return its metadata in the JSON format.

    Examples: \n
    \t $ cernopendata-client get-metadata --recid 1\n
    \t $ cernopendata-client get-metadata --recid 1 --output-value title\n
    \t $ cernopendata-client get-metadata --recid 329 --output-value authors.orcid --filter name="Rousseau, David"
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    output_json = record_json["metadata"]
    if output_value:
        fields = output_value.split(".")
        wrong_field = True
        try:
            for field in fields:
                output_json = output_json[field]
            if filters:
                filter_metadata(field, filters, output_json)
                return
        except (KeyError, TypeError):
            try:
                if filters:
                    filter_metadata(field, filters, output_json)
                    wrong_field = False
                else:
                    for object in output_json:
                        if field in object:
                            wrong_field = False
                            display_message(msg=object[field])
            except (KeyError, TypeError):
                handle_error_message(field)
            if wrong_field:
                handle_error_message(field)
            return

        if isinstance(output_json, (dict, list)):
            display_message(msg=json.dumps(output_json, indent=4))
        else:  # print strings or numbers more simply
            display_message(msg=output_json)
    elif filters:
        display_message(
            msg_type="error",
            msg="--filter can only be used with --output-value",
        )
    else:
        display_message(msg=json.dumps(output_json, indent=4))


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID (exact match)")
@click.option("--doi", help="Digital Object Identifier (exact match)")
@click.option("--title", help="Record title (exact match, no wildcards)")
@click.option(
    "--protocol",
    default="http",
    type=click.Choice(["http", "xrootd"]),
    help="Protocol to be used in links [http,xrootd]",
)
@click.option(
    "--expand/--no-expand", default=True, help="Expand file indexes? [default=yes]"
)
@click.option(
    "--server",
    default=SERVER_HTTP_URI,
    type=click.STRING,
    help="Which CERN Open Data server to query? [default={}]".format(SERVER_HTTP_URI),
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Output also the file size (in the second column) and the file checksum (in the third column).",
)
def get_file_locations(server, recid, doi, title, protocol, expand, verbose):
    """Get a list of data file locations of a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and return the list of data file locations
    belonging to this record.

    Examples: \n
    \t $ cernopendata-client get-file-locations --recid 5500\n
    \t $ cernopendata-client get-file-locations --recid 5500 --protocol xrootd\n
    \t $ cernopendata-client get-file-locations --recid 5500 --verbose
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    file_locations = get_files_list(server, record_json, protocol, expand, verbose)
    if verbose:
        for file_ in file_locations:
            display_message(msg="{}\t{}\t{}".format(file_[0], file_[1], file_[2]))
    else:
        for file_ in file_locations:
            display_message(msg="{}".format(file_[0]))


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID (exact match)")
@click.option("--doi", help="Digital Object Identifier (exact match)")
@click.option("--title", help="Record title (exact match, no wildcards)")
@click.option(
    "--protocol",
    default="http",
    type=click.Choice(["http", "xrootd"]),
    help="Protocol to be used in links [http,xrootd]",
)
@click.option(
    "--expand/--no-expand", default=True, help="Expand file indexes? [default=yes]"
)
@click.option(
    "--server",
    default=SERVER_HTTP_URI,
    type=click.STRING,
    help="Which CERN Open Data server to query? [default={}]".format(SERVER_HTTP_URI),
)
@click.option(
    "--dry-run",
    "dryrun",
    is_flag=True,
    default=False,
    help="Do not download anything, only print out data file locations to be downloaded",
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
@click.option(
    "--verify/--no-verify",
    "verify",
    default=True,
    help="Verify downloaded data file checksums when available [default=yes]",
)
@click.option(
    "--retry-limit",
    "retry_limit",
    default=DOWNLOAD_RETRY_LIMIT,
    type=click.INT,
    help="Number of retries when downloading a file [default={}]".format(
        DOWNLOAD_RETRY_LIMIT
    ),
)
@click.option(
    "--retry-sleep",
    "retry_sleep",
    default=DOWNLOAD_RETRY_SLEEP,
    type=click.INT,
    help="Sleep time in seconds before retrying downloads [default={}]".format(
        DOWNLOAD_RETRY_SLEEP
    ),
)
@click.option(
    "--download-engine",
    "download_engine",
    type=click.Choice(["requests", "pycurl", "xrootd"]),
    help="Download engine to use when downloading files."
    "The available values are 'requests', 'pycurl', 'xrootd'."
    "[default=requests (for HTTP protocol), xrootd (for XRootD protocol)]",
)
def download_files(
    server,
    recid,
    doi,
    title,
    protocol,
    expand,
    names,
    regexp,
    ranges,
    dryrun,
    verify,
    retry_limit,
    retry_sleep,
    download_engine,
):
    """Download data files belonging to a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and download data files belonging to this record.

    Examples: \n
    \t $ cernopendata-client download-files --recid 5500\n
    \t $ cernopendata-client download-files --recid 5500 --filter-name BuildFile.xml\n
    \t $ cernopendata-client download-files --recid 5500 --filter-regexp py$\n
    \t $ cernopendata-client download-files --recid 5500 --filter-range 1-4\n
    \t $ cernopendata-client download-files --recid 5500 --filter-range 1-2,5-7\n
    \t $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range 1-2
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    if retry_limit:
        validate_retry_limit(retry_limit=retry_limit)
    if retry_sleep:
        validate_retry_sleep(retry_sleep=retry_sleep)
    # Get record metadata and resolve recid from DOI/title if needed
    record_json = get_record_as_json(server, recid, doi, title)
    record_recid = record_json["metadata"]["recid"]
    file_entries = get_file_entries(server, record_json, protocol, expand)
    file_locations = [entry.uri for entry in file_entries]
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
            filtered_files=download_file_locations if names else None,
        )
        download_file_locations = dload_file_location_regexp
    if ranges:
        parsed_range_filters = parse_parameters(ranges)
        dload_file_location_range = get_download_files_by_range(
            ranges=parsed_range_filters,
            file_locations=file_locations,
            filtered_files=download_file_locations if names or regexp else None,
        )
        download_file_locations = dload_file_location_range

    if names or regexp or ranges:
        if not download_file_locations:
            display_message(
                msg_type="error",
                msg="No files matching the filters",
            )
            sys.exit(1)
    else:
        download_file_locations = file_locations

    file_entries_by_location = {entry.uri: entry for entry in file_entries}
    download_file_entries = [
        file_entries_by_location[file_location]
        for file_location in download_file_locations
    ]

    if dryrun:
        display_message(msg="\n".join(download_file_locations))
        sys.exit(0)

    total_files = len(download_file_locations)
    base_path = str(record_recid)
    if not os.path.isdir(base_path):
        try:
            os.mkdir(base_path)
        except OSError:
            display_message(
                msg_type="error",
                msg="Creation of the directory {} failed".format(base_path),
            )
    download_items = get_download_items(
        base_path, download_file_entries, layout_entries=file_entries
    )
    if not download_engine:
        if protocol.startswith("http"):
            download_engine = "requests"
        elif protocol == "xrootd":
            download_engine = "xrootd"
    for file_number, download_item in enumerate(download_items, start=1):
        os.makedirs(download_item.destination_directory, exist_ok=True)
        display_message(
            msg_type="info",
            msg="Downloading file {} of {}".format(file_number, total_files),
        )
        download_single_file(
            path=download_item.destination_directory,
            file_location=download_item.file_location,
            protocol=protocol,
            download_engine=download_engine,
            expected_size=download_item.expected_size,
        )
        check_error(
            path=download_item.destination_directory,
            file_location=download_item.file_location,
            protocol=protocol,
            retry_limit=retry_limit,
            retry_sleep=retry_sleep,
            download_engine=download_engine,
        )
        verify_downloaded_file(
            download_item.destination_path,
            expected_size=download_item.expected_size,
            expected_checksum=download_item.expected_checksum,
            verify_checksum=verify,
        )
        if download_item.is_file_index:
            display_message(
                msg_type="note",
                msg=(
                    "Skipping metadata size and checksum checks for the "
                    "unexpanded file-index response."
                ),
            )
    display_message(
        msg_type="info",
        msg="Success!",
    )


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID (exact match)")
@click.option("--doi", help="Digital Object Identifier (exact match)")
@click.option("--title", help="Record title (exact match, no wildcards)")
@click.option(
    "--server",
    default=SERVER_HTTP_URI,
    type=click.STRING,
    help="Which CERN Open Data server to query? [default={}]".format(SERVER_HTTP_URI),
)
def verify_files(server, recid, doi, title):
    """Verify downloaded data file integrity.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and verify integrity of downloaded data files
    belonging to this record.

    Examples: \n
    \t $ cernopendata-client verify-files --recid 5500
    """
    # Validate parameters
    validate_server(server)
    if recid is not None:
        validate_recid(recid)

    # Get record metadata and resolve recid from DOI/title if needed
    record_json = get_record_as_json(server, recid, doi, title)
    record_recid = record_json["metadata"]["recid"]

    file_entries = get_file_entries(
        server=server,
        record_json=record_json,
        protocol=server.split(":", 1)[0],
        expand=True,
    )
    download_items = get_download_items(str(record_recid), file_entries)

    # Get local file information
    local_file_paths = get_local_file_paths(str(record_recid))
    if not local_file_paths:
        display_message(
            msg_type="error",
            msg="No local files found for record {}. Perhaps run `download-files` first? Exiting.".format(
                record_recid
            ),
        )
        sys.exit(1)

    # Verify number of files
    display_message(
        msg_type="info",
        msg="Verifying number of files for record {}... ".format(record_recid),
    )
    display_message(
        msg_type="note",
        msg="Expected {}, found {}".format(len(download_items), len(local_file_paths)),
    )
    if len(download_items) != len(local_file_paths):
        display_message(
            msg_type="error",
            msg="File count does not match.",
        )
        sys.exit(1)

    # Verify size and checksum of each exact destination
    for download_item in download_items:
        verify_downloaded_file(
            download_item.destination_path,
            expected_size=download_item.expected_size,
            expected_checksum=download_item.expected_checksum,
        )

    # Success!
    display_message(
        msg_type="info",
        msg="Success!",
    )


@cernopendata_client.command()
@click.option(
    "-R",
    "--recursive",
    "recursive",
    is_flag=True,
    default=False,
    help="Iterate recursively in the given directory path",
)
@click.option(
    "--timeout",
    default=LIST_DIRECTORY_TIMEOUT,
    type=click.INT,
    help="Timeout after which to exit running the command [default={}]".format(
        LIST_DIRECTORY_TIMEOUT
    ),
)
@click.argument("path", type=click.STRING)
def list_directory(path, recursive, timeout):
    """List contents of a EOSPUBLIC Open Data directory.

    Returns the list of files and subdirectories of a given EOSPUBLIC directory.

    Examples: \n
    \t $ cernopendata-client list-directory /eos/opendata/cms/validated-runs/Commissioning10\n
    \t $ cernopendata-client list-directory /eos/opendata/cms/Run2010B/BTau/AOD --recursive\n
    \t $ cernopendata-client list-directory /eos/opendata/cms/Run2010B --recursive --timeout 10
    """
    validate_directory(directory=path)
    files = get_list_directory(path, recursive, timeout)
    if not files:
        display_message(
            msg_type="info",
            msg="No files in the directory.",
        )
        sys.exit(2)
    display_message(msg="\n".join(files))
