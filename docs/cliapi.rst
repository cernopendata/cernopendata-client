.. _cliapi:

CLI API
=======

.. code-block:: console

    $ cernopendata-client --help
    Usage: cernopendata-client [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    download-files      Download data files belonging to a record.
    get-file-locations  Get a list of data file locations of a record.
    get-metadata        Get metadata content of a record.
    list-directory      List contents of a EOSPUBLIC Open Data directory.
    verify-files        Verify downloaded data file integrity.
    version             Return cernopendata-client version.

.. click:: cernopendata_client.cli:cernopendata_client
   :prog: cernopendata-client
   :nested: full
