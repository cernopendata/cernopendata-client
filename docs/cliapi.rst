CLI API
=======

General help
------------

In order to get help for any ``cernopendata-client`` command, use the
``--help`` option:

.. code-block:: console

    $ cernopendata-client --help
    Usage: cernopendata-client [OPTIONS] COMMAND [ARGS]...

    Options:
    --help  Show this message and exit.

    Commands:
    download-files      Download data files belonging to a record.
    get-file-locations  Get a list of data file locations of a record.
    get-metadata        Get metadata content of a record.
    verify-files        Verify downloaded data file integrity.
    version             Return cernopendata-client version.

.. _cliapi:

.. click:: cernopendata_client.cli:cernopendata_client
   :prog: cernopendata-client
   :nested: full
