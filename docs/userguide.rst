.. _gettingstarted:

User Guide
===============

Install cernopendata-client
---------------------------

If you are interested in exploring resources of opendata.cern.ch from cli,
all you need to install is the ``cernopendata-client``,
ideally in a new virtual environment:

.. code-block:: console

   $ # create new virtual environment
   $ virtualenv ~/.virtualenvs/cernopendata_client
   $ source ~/.virtualenvs/cernopendata_client/bin/activate
   $ # install cernopendata-client
   $ pip install cernopendata-client

Basic usage
-----------

.. code-block:: console

    $ # get a record
    $ cernopendata-client get-record --recid 43
    $ ...
    $ # you can get a record by title or doi as well
    $ cernopendata-client get-record --title /Mu/Run2010B-v1/RAW
    $ ...
    $ cernopendata-client get-record --doi 10.7483/OPENDATA.CMS.W24L.SGYC
    $ ...

    $ # if you need only some fields from the record you can use
    $ # the --output-fields option:
    $ cernopendata-client get-record --recid 43 --output-fields id,links
    $ ...

    $ # Note that only top-level fields can be used with this option,
    $ # For deeper and more complex queries you can use jq."
    $ #  For example to get the field global_tag that is nested deeper:
    $ cernopendata-client get-record --recid 43 | jq ".metadata.system_details.global_tag"


    $ # To get a list of files belonging to a dataset you can use the get-file-locations
    $ cernopendata-client get-file-locations --recid 43
    $ ...
    $ # Using --title and --doi is also possible here.
    $
    $ # By default links are in root protocol, but if you can change it
    $ # with --protocol option:
    $ cernopendata-client get-file-locations --recid 43 --protocol http
    $ ...


CLI API
-------

.. click:: cernopendata_client.cli:get_record
   :prog: get_record
   :show-nested:

.. click:: cernopendata_client.cli:get_file_locations
   :prog: get_file_locations
   :show-nested:
