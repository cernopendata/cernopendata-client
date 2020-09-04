# -*- coding: utf-8 -*-
# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

from __future__ import print_function

import argparse
import os
import sys

import click
import requests

try:
    from urllib.parse import quote
except ImportError:
    # fallback for Python 2
    from urllib import quote


def verify_recid(server=None, recid=None):
    """Verify that recid corresponds to a valid Open Data record webpage."""
    if recid is None:
        sys.exit(
            "ERROR: You must supply a record id number as an " "input using -r flag."
        )
    else:
        input_record_url = server + "/record/" + str(recid)
        input_record_url_check = requests.get(input_record_url)

        if input_record_url_check.status_code == 200:
            base_record_id = str(recid)
            return base_record_id
        else:
            try:
                input_record_url_check.raise_for_status()
            except requests.HTTPError as http_error_msg:
                print("ERROR: The record id number you supplied is not valid.")
                sys.exit(http_error_msg)
            return False


def get_recid_api(server=None, base_record_id=None):
    """Get the api for the record with given recid."""
    record_api_url = server + "/api/records/" + base_record_id
    record_api = requests.get(record_api_url)
    record_api.raise_for_status()
    return record_api


def get_recid(server=None, title=None, doi=None):
    """Get record id by either title or doi."""
    if title:
        name, value = "title", title
    elif doi:
        name, value = "doi", doi
    url = (
        server
        + "?page=1&size=1&q={}:".format(name)
        + quote('"{}"'.format(value), safe="")
    )
    response = requests.get(url)
    response_json = response.json()
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        click.secho("Connection to server failed: \n reason: {}.".format(e), err=True)
    if "hits" in response_json:
        hits_total = response_json["hits"]["total"]
        if hits_total < 1:
            click.secho(
                "Record with given {} does not exist.".format(name), fg="red", err=True
            )
            sys.exit(2)
        elif hits_total > 1:
            click.secho(
                "More than one record fit this {}."
                "This should not happen.".format(name),
                fg="red",
                err=True,
            )
            sys.exit(3)
        elif hits_total == 1:
            return response_json["hits"]["hits"][0]["id"]


def get_record_as_json(server=None, recid=None, doi=None, title=None):
    """Get record content in json by its recid, doi or title."""
    if recid:
        record_id = recid
    elif title:
        record_id = get_recid(server=server, title=title)
    elif doi:
        record_id = get_recid(server=server, doi=doi)
    else:
        click.secho(
            "Please provide at least one of following arguments: "
            "(recid, doi, title)",
            fg="red",
            err=True,
        )
        sys.exit(1)

    record_id = verify_recid(server=server, recid=record_id)
    record_api = get_recid_api(server=server, base_record_id=record_id)
    return record_api.json()


def get_files_list(server=None, record_json=None, protocol=None, expand=None):
    """Get file list of a dataset by its recid, doi, or title."""
    files_list = [file["uri"] for file in record_json["metadata"]["files"]]
    if expand:
        # let's unwind file indexes
        files_list_expanded = []
        for file_ in files_list:
            if file_.endswith("_file_index.txt"):
                url_file = file_.replace("root://eospublic.cern.ch/", server)
                req = requests.get(url_file)
                for url_individual_file in req.text.split("\n"):
                    if url_individual_file:
                        files_list_expanded.append(url_individual_file)
            elif file_.endswith("_file_index.json"):
                pass
            else:
                files_list_expanded.append(file_)
        files_list = files_list_expanded

    if protocol == "http":
        files_list = [
            file_.replace("root://eospublic.cern.ch/", server) for file_ in files_list
        ]

    return files_list
