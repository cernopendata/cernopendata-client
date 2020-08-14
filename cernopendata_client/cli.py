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

from cernopendata_client.opendata_analysis_query import (get_recid_api,
                                                         verify_recid)

try:
    from urllib.parse import quote
except ImportError:
    # fallback for Python 2
    from urllib import quote

SEARCH_URL = 'http://opendata.cern.ch/api/records/'


def validate_recid(recid):
    if recid <= 0:
        raise click.BadParameter(
            'Recid should be a positive integer',
            param_hint=["--recid"],
        )

@click.group()
def cernopendata_client():
    pass


@cernopendata_client.command()
@click.option('--recid',
              type=click.INT,
              help='Record ID')
@click.option('--doi',
              help='Digital Object Identifier.')
@click.option('--title',
              help='Record title')
@click.option('--output-fields', is_flag=False, type=click.STRING,
              help='Comma separated list of fields from the record '
                   'that should be included in the output.')
def get_record(recid, doi, title, output_fields):
    """Get records content by its recid, doi or title filtered."""
    # TODO: Add decorator to require one of (recid, doi or title)
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(recid, doi, title)
    if output_fields is not None:
        output_fields = [f.strip() for f in output_fields.split(',')]
    if output_fields and len(output_fields) > 0:
        try:
            output_json = {
                field: record_json[field] for field in output_fields
            }
        except KeyError:
            top_level_fields = ', '.join(field for field in record_json)
            click.secho("Provided field is not top level field of this record."
                        "\nFor this record top level fields are: {}"
                        "\n\nFor deeper more complex queries you can use jq "
                        "(see documentation for examples).".format(
                            top_level_fields
                        ), fg='red', err=True)
            sys.exit()
    else:
        output_json = record_json
    click.echo(json.dumps(output_json, indent=4))


@cernopendata_client.command()
@click.option('--recid',
              type=click.INT,
              help='Record ID')
@click.option('--doi',
              help='Digital Object Identifier.')
@click.option('--title',
              help='Record title')
@click.option('--protocol', default='root',
              type=click.Choice(['root', 'http']),
              help='Protocol to be used in links.')
@click.option('--expand/--no-expand', default=True,
              help='Expand file indexes? [default=yes]')
def get_file_locations(recid, doi, title, protocol, expand):
    """Get a list of files belonging to a dataset."""
    if recid is not None:
        validate_recid(recid)
    record_json = get_record_as_json(recid, doi, title)
    file_locations = [
        file['uri'] for file in record_json['metadata']['files']
    ]
    if expand:
        # let's unwind file indexes
        file_locations_expanded = []
        for file in file_locations:
            if file.endswith('_file_index.txt'):
                url_file = file.replace('root://eospublic.cern.ch/', 'http://opendata.cern.ch')
                req = requests.get(url_file)
                for url_individual_file in req.text.split('\n'):
                    if url_individual_file:
                        file_locations_expanded.append(url_individual_file)
            elif file.endswith('_file_index.json'):
                pass
            else:
                file_locations_expanded.append(file)
        file_locations = file_locations_expanded

    if protocol == 'http':
        file_locations = [
            f.replace('root://eospublic.cern.ch/', 'http://opendata.cern.ch')
            for f in file_locations
        ]
    click.echo('\n'.join(file_locations))


def get_recid(title=None, doi=None):
    """Get record id by either title or doi."""
    if title:
        name, value = 'title', title
    elif doi:
        name, value = 'doi', doi
    url = (SEARCH_URL + "?page=1&size=1&q={}:".format(name)
           + quote('"{}"'.format(value), safe=''))
    response = requests.get(url)
    try:
        response.raise_for_status()
    except HTTPError as e:
        click.secho('Connection to server failed: \n reason: {}.'.format(e),
                    err=True)
    if 'hits' in response.json():
        hits_total = response.json()['hits']['total']
        if hits_total < 1:
            click.secho('Record with given {} does not exist.'.format(name),
                        fg='red', err=True)
            sys.exit()
        elif hits_total > 1:
            click.secho('More than one record fit this {}.'
                        ' This should not happen.'.format(name),
                        fg='red', err=True)
            sys.exit()
        elif hits_total == 1:
            return response.json()['hits']['hits'][0]['id']


def get_record_as_json(recid, doi, title):
    """Get record content in json by its recid, doi or title."""
    if recid:
        record_id = recid
    elif title:
        record_id = get_recid(title=title)
    elif doi:
        record_id = get_recid(doi=doi)
    else:
        click.secho("Please provide at least one of following arguments: "
                    "(recid, doi, title)", fg='red', err=True)
        sys.exit()

    record_id = verify_recid(record_id)
    record_api = get_recid_api(record_id)
    return record_api.json()
