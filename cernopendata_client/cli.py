# TODO: add licence

import os
import sys

import click


@click.group()
def cernopendata_client():
    pass


@cernopendata_client.command()
@click.option('--recid',
              help='Record ID')
@click.option('--doi',
              help='.') # TODO
@click.option('--title',
              help='Record Title')
@click.option('--output-fields',
              help='Fields that should be included in the output.')
def get_record(recid, doi, title, output_fields):
    # TODO: Add decorator to require one of (recid, doi or title)
    # TODO: add logic
    raise NotImplementedError()


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
    # TODO: add logic
    # TODO: Add decorator to require one of (recid, doi or title)
    raise NotImplementedError()
