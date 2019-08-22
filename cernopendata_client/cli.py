# TODO: add licence
import json
import urllib.parse

import click
import requests
from requests import HTTPError

from cernopendata_client.opendata_analysis_query import verify_recid, \
    get_recid_api

SEARCH_URL = 'http://opendata.cern.ch/api/records/'

@click.group()
def cernopendata_client():
    pass


@cernopendata_client.command()
@click.option('--recid',
              help='Record ID')
@click.option('--doi',
              help='Digital Object Identifier.')
@click.option('--title',
              help='Record Title')
@click.option('--output-fields', is_flag=False, type=click.STRING,
              help='Fields from the record that should be included '
                   'in the output. (i.e. id, metadata or links)')
def get_record(recid, doi, title, output_fields):
    """Get records content by its recid, doi or title."""
    if output_fields is not None:
        output_fields = [f.strip() for f in output_fields.split(',')]

    # TODO: Add decorator to require one of (recid, doi or title)
    if recid:
        record_id = recid
    elif title:
        record_id = get_recid(title=title)
    elif doi:
        record_id = get_recid(doi=doi)
    else:
        click.secho("Please provide at least one of following arguments: "
                    "(recid, doi, title)", fg='red', err=True)
        return 1

    record_id = verify_recid(record_id)
    record_api = get_recid_api(record_id)
    record_json = record_api.json()
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
            return 1
    else:
        output_json = record_json
    click.echo(json.dumps(output_json, indent=4))


@cernopendata_client.command()
@click.option('--recid',
              help='Record ID')
@click.option('--doi',
              help='.') #TODO
@click.option('--title',
              help='Record ID')
@click.option('--protocol',
              help='Root or default.')
def get_file_locations(url, wget_options, out_warc_file, directory_prefix):
    """
    :param url:
    :param wget_options:
    :param out_warc_file:
    :param directory_prefix:
    """
    # TODO: add logic
    # TODO: Add decorator to require one of (recid, doi or title)
    raise NotImplementedError()


def get_recid(title=None, doi=None):
    """Get record id by either title or doi."""
    if title:
        name, value = 'title', title
    elif doi:
        name, value = 'doi', doi
    url = (SEARCH_URL + "?page=1&size=1&q={}:".format(name)
           + urllib.parse.quote('"{}"'.format(value), safe=''))
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
            return 1
        elif hits_total > 1:
            click.secho('More than one record fit this {}.'
                        ' This should not happen.'.format(name),
                        fg='red', err=True)
            return 1
        elif hits_total == 1:
            return response.json()['hits']['hits'][0]['id']
