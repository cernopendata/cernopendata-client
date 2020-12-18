# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""cernopendata-client record search related utilities."""

from __future__ import print_function

import sys
import requests

from .config import SERVER_HTTP_URI, SERVER_ROOT_URI, SERVER_HTTPS_URI
from .printer import display_message

try:
    from urllib.parse import quote
except ImportError:
    # fallback for Python 2
    from urllib import quote


def verify_recid(server=None, recid=None):
    """Verify that recid corresponds to a valid Open Data record webpage.

    :param server: CERN Open Data server to query
    :param recid: Record ID
    :type server: str
    :type recid: int

    :return: Boolean after verifying the record ID
    :rtype: bool
    """
    input_record_url = server + "/record/" + str(recid)
    input_record_url_check = requests.get(input_record_url)

    if input_record_url_check.status_code == 200:
        base_record_id = str(recid)
        return base_record_id
    else:
        try:
            input_record_url_check.raise_for_status()
        except Exception:
            display_message(
                msg_type="error",
                msg="The record ID number you supplied is not valid.",
            )
            sys.exit(1)
        return False


def get_recid_api(server=None, base_record_id=None):
    """Return api for the record with given recid.

    :param server: CERN Open Data server to query
    :param base_record_id: Record ID
    :type server: str
    :type base_record_id: int

    :return: String of record api
    :rtype: str
    """
    record_api_url = server + "/api/records/" + base_record_id
    record_api = requests.get(record_api_url)
    try:
        record_api.raise_for_status()
    except Exception:
        display_message(
            msg_type="error",
            msg="The record ID number you supplied is not valid.",
        )
        sys.exit(1)
    return record_api


def get_recid(server=None, title=None, doi=None):
    """Return record ID by either title or doi.

    :param server: CERN Open Data server to query
    :param title: Record title
    :param doi: Digital Object Identifier of record
    :type server: str
    :type title: str
    :type doi: str

    :return: record ID
    :rtype: int
    """
    if title:
        name, value = "title", title
    elif doi:
        name, value = "doi", doi
    url = (
        server
        + "/api/records"
        + "?page=1&size=1&q={}:".format(name)
        + quote('"{}"'.format(value), safe="")
    )
    response = requests.get(url)
    response_json = response.json()
    try:
        response.raise_for_status()
    except Exception as e:
        display_message(
            msg_type="error",
            msg="Connection to server failed: \n reason: {}.".format(e),
        )
    if "hits" in response_json:
        hits_total = response_json["hits"]["total"]
        if hits_total < 1:
            display_message(
                msg_type="error",
                msg="Record with given {} does not exist.".format(name),
            )
            sys.exit(2)
        elif hits_total > 1:
            display_message(
                msg_type="error",
                msg="More than one record fit this {}."
                "This should not happen.".format(name),
            )
            sys.exit(3)
        elif hits_total == 1:
            return response_json["hits"]["hits"][0]["id"]


def get_record_as_json(server=None, recid=None, doi=None, title=None):
    """Return record content in json by its recid, doi or title.

    :param server: CERN Open Data server to query
    :param recid: Record ID
    :param title: Record title
    :param doi: Digital Object Identifier of record
    :type server: str
    :type recid: int
    :type title: str
    :type doi: str

    :return: record content in JSON
    :rtype: json(dict)
    """
    if recid:
        record_id = recid
    elif title:
        record_id = get_recid(server=server, title=title)
    elif doi:
        record_id = get_recid(server=server, doi=doi)
    else:
        display_message(
            msg_type="error",
            msg="Please provide at least one of following arguments: "
            "(recid, doi, title)",
        )
        sys.exit(1)

    record_id = verify_recid(server=server, recid=record_id)
    record_api = get_recid_api(server=server, base_record_id=record_id)
    record_json = record_api.json()
    if "_files" in record_json["metadata"]:
        del record_json["metadata"]["_files"]
    try:
        if record_json["metadata"]["files"]:
            for field in record_json["metadata"]["files"]:
                if "bucket" in field:
                    del field["bucket"]
                if "version_id" in field:
                    del field["version_id"]
    except KeyError:
        record_json["metadata"]["files"] = []
    return record_json


def get_files_list(
    server=None, record_json=None, protocol=None, expand=None, verbose=None
):
    """Return file list of a dataset by its recid, doi, or title.

    :param server: CERN Open Data server to query
    :param record_json: Record content in JSON
    :protocol: Protocol to be used in links [http,xrootd]
    :expand: Flag for expanding file indexes
    :verbose: Flag for showing size and checksum of file
    :type server: str
    :type record_json: json(dict)
    :type protocol: str
    :type expand: bool
    :type verbose: bool

    :return: List of files list
    :rtype: list
    """
    searcher_protocol = protocol
    if server != SERVER_HTTP_URI and searcher_protocol != "xrootd":
        searcher_protocol = server.split(":")[0]
    files_list = []
    for file_ in record_json["metadata"]["files"]:
        files_list.append((file_["uri"], file_["size"], file_["checksum"]))
    if expand:
        # let's unwind file indexes
        files_list_expanded = []
        for file_ in files_list:
            if file_[0].endswith("_file_index.json"):
                try:
                    url_file = "{}/record/{}/files/{}".format(
                        server, str(record_json["id"]), file_[0].split("/")[-1]
                    )
                    json_files = requests.get(url_file).json()
                except Exception:
                    display_message(
                        msg_type="error",
                        msg="Error occured while fetching file info. Please try again.",
                    )
                    sys.exit(1)
                for file_ in json_files:
                    files_list_expanded.append(
                        (
                            file_["uri"],
                            file_["size"],
                            file_["checksum"],
                        )
                    )
            elif file_[0].endswith("_file_index.txt"):
                pass
            else:
                files_list_expanded.append(file_)
        files_list = files_list_expanded
    if searcher_protocol == "http":
        files_list = [
            (file_[0].replace(SERVER_ROOT_URI, server), file_[1], file_[2])
            for file_ in files_list
        ]
    elif searcher_protocol == "https":
        files_list = [
            (
                file_[0].replace(SERVER_ROOT_URI, SERVER_HTTPS_URI),
                file_[1],
                file_[2],
            )
            for file_ in files_list
        ]
    return files_list


def get_file_info_remote(server, recid, protocol=None, filtered_files=None):
    """Return remote file information list for given record.

    :param server: CERN Open Data server to query
    :param recid: Record ID
    :param filtered_files: list of file locations after applying filters(if any)
    :type server: str
    :type recid: int
    :type filtered_files: list

    :return: Returns a list of dictionaries containing (checksum, name, size,
    uri) for each file in the record.  Note that 'name' property is
    not stored remotely, but is calculated in this function for
    convenience.
    :rtype: list
    """
    searcher_protocol = protocol
    file_info_remote = []
    if server != SERVER_HTTP_URI and searcher_protocol != "xrootd":
        searcher_protocol = server.split(":")[0]
    record_json = get_record_as_json(server=server, recid=recid)
    for file_info in record_json["metadata"]["files"]:
        file_checksum = file_info["checksum"]
        file_size = file_info["size"]
        file_uri = file_info["uri"]
        file_name = file_info["uri"].rsplit("/", 1)[1]
        if searcher_protocol == "http":
            file_uri = file_info["uri"].replace(SERVER_ROOT_URI, server)
        elif searcher_protocol == "https":
            file_uri = file_info["uri"].replace(SERVER_ROOT_URI, SERVER_HTTPS_URI)
        if not filtered_files or file_uri in filtered_files:
            file_info_remote.append(
                {
                    "checksum": file_checksum,
                    "name": file_name,
                    "size": file_size,
                    "uri": file_uri,
                }
            )
    return file_info_remote
