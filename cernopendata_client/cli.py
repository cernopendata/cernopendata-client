# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2019, 2020, 2021 CERN.
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
    check_error,
    download_single_file,
    get_download_files_by_name,
    get_download_files_by_range,
    get_download_files_by_regexp,
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
from .verifier import get_file_info_local, verify_file_info
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

    \b
    Examples:
      $ cernopendata-client version
    """
    display_message(msg=__version__)


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier")
@click.option("--title", help="Title of the record")
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
def get_metadata(server, recid, doi, title, output_value):
    # noqa: D301
    """Get metadata content of a record.

    Select a CERN Open Data bibliographic record by a record ID, a
    DOI, or a title and return its metadata in the JSON format.

    \b
    Examples:
      $ cernopendata-client get-metadata --recid 1
      $ cernopendata-client get-metadata --recid 1 --output-value title
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(server, recid, doi, title)
    output_json = record_json["metadata"]
    if not output_value:
        display_message(msg=json.dumps(output_json, indent=4))
    else:
        fields = output_value.split(".")
        for field in fields:
            try:
                output_json = output_json[field]
            except (KeyError, TypeError):
                display_message(
                    msg_type="error",
                    msg="Field '{}' is not present in metadata".format(field),
                )
                sys.exit(1)
        if type(output_json) is dict or type(output_json) is list:
            display_message(msg=json.dumps(output_json, indent=4))
        else:  # print strings or numbers more simply
            display_message(msg=output_json)


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier")
@click.option("--title", help="Record title")
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

    \b
    Examples:
      $ cernopendata-client get-file-locations --recid 5500
      $ cernopendata-client get-file-locations --recid 5500 --protocol xrootd
      $ cernopendata-client get-file-locations --recid 5500 --verbose
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
@click.option("--recid", type=click.INT, help="Record ID")
@click.option("--doi", help="Digital Object Identifier")
@click.option("--title", help="Record title")
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
    "--verify",
    "verify",
    is_flag=True,
    default=False,
    help="Verify downloaded data file integrity",
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

    \b
    Examples:
      $ cernopendata-client download-files --recid 5500
      $ cernopendata-client download-files --recid 5500 --filter-name BuildFile.xml
      $ cernopendata-client download-files --recid 5500 --filter-regexp py$
      $ cernopendata-client download-files --recid 5500 --filter-range 1-4
      $ cernopendata-client download-files --recid 5500 --filter-range 1-2,5-7
      $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range 1-2
    """
    validate_server(server)
    if recid is not None:
        validate_recid(recid)
    if retry_limit:
        validate_retry_limit(retry_limit=retry_limit)
    if retry_sleep:
        validate_retry_sleep(retry_sleep=retry_sleep)
    record_json = get_record_as_json(server, recid, doi, title)
    file_locations_info = get_files_list(server, record_json, protocol, expand)
    file_locations = [file_[0] for file_ in file_locations_info]
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

    if dryrun:
        display_message(msg="\n".join(download_file_locations))
        sys.exit(0)

    total_files = len(download_file_locations)
    path = str(recid)
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError:
            display_message(
                msg_type="error",
                msg="Creation of the directory {} failed".format(path),
            )
    if not download_engine:
        if protocol.startswith("http"):
            download_engine = "requests"
        elif protocol == "xrootd":
            download_engine = "xrootd"
    for file_location in download_file_locations:
        display_message(
            msg_type="info",
            msg="Downloading file {} of {}".format(
                download_file_locations.index(file_location) + 1, total_files
            ),
        )
        download_single_file(
            path=path,
            file_location=file_location,
            protocol=protocol,
            download_engine=download_engine,
        )
        check_error(
            path=path,
            file_location=file_location,
            protocol=protocol,
            retry_limit=retry_limit,
            retry_sleep=retry_sleep,
        )
        if verify:
            file_info_remote = get_file_info_remote(
                server,
                recid,
                protocol=protocol,
                filtered_files=[file_location],
            )
            file_info_local = get_file_info_local(recid)
            verify_file_info(file_info_local, file_info_remote)
    display_message(
        msg_type="info",
        msg="Success!",
    )


@cernopendata_client.command()
@click.option("--recid", type=click.INT, help="Record ID")
@click.option(
    "--server",
    default=SERVER_HTTP_URI,
    type=click.STRING,
    help="Which CERN Open Data server to query? [default={}]".format(SERVER_HTTP_URI),
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
    validate_server(server)
    if recid is not None:
        validate_recid(recid)

    # Get remote file information
    file_info_remote = get_file_info_remote(server, recid)

    # Get local file information
    file_info_local = get_file_info_local(recid)
    if not file_info_local:
        display_message(
            msg_type="error",
            msg="No local files found for record {}. Perhaps run `download-files` first? Exiting.".format(
                recid
            ),
        )
        sys.exit(1)

    # Verify number of files
    display_message(
        msg_type="info",
        msg="Verifying number of files for record {}... ".format(recid),
    )
    display_message(
        msg_type="note",
        msg="Expected {}, found {}".format(len(file_info_remote), len(file_info_local)),
    )
    if len(file_info_remote) != len(file_info_local):
        display_message(
            msg_type="error",
            msg="File count does not match.",
        )
        sys.exit(1)

    # Verify size and checksum of each file
    verify_file_info(file_info_local, file_info_remote)

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

    \b
    Examples:
      $ cernopendata-client list-directory /eos/opendata/cms/validated-runs/Commissioning10
      $ cernopendata-client list-directory /eos/opendata/cms/Run2010B/BTau/AOD --recursive
      $ cernopendata-client list-directory /eos/opendata/cms/Run2010B --recursive --timeout 10
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
