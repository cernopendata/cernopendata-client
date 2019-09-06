=========================
 CERN Open Data - Client
=========================

.. image:: https://img.shields.io/pypi/pyversions/cernopendata-client.svg
   :target: https://pypi.org/pypi/cernopendata-client

.. image:: https://img.shields.io/travis/cernopendata/cernopendata-client.svg
   :target: https://travis-ci.org/cernopendata/cernopendata-client

.. image:: https://readthedocs.org/projects/cernopendata-client/badge/?version=latest
   :target: https://cernopendata-client.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/coveralls/cernopendata/cernopendata-client.svg
   :target: https://coveralls.io/r/cernopendata/cernopendata-client

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/cernopendata/opendata.cern.ch?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/github/license/cernopendata/cernopendata-client.svg
   :target: https://github.com/cernopendata/cernopendata-client/blob/master/LICENSE

About
=====

The CERN Open Data Client is a command line tool used to better facilitate
the individual acquisition of files from the
`CERN Open Data Portal <http://opendata.cern.ch/>`_.
The tool uses the portal's API to query a given Open Data record
and automatically download the files listed on that record.
In its current form, the tool can only be used for analysis records like the
`Higgs-to-four-lepton analysis example <http://opendata.cern.ch/record/5500/>`_,
but it should be generalized in the future to work for any type
of Open Data portal record.


Usage
=====

To use this command line tool simply run the program from the command lin
using python as shown below. The program requires the user to provide
a CERN Open Data portal record number using the ``-r`` flag.
The record number of a Open Data portal record is simply found at the end of
the URL for that record (e.g. the record number for the Two-lepton/four-lepton
analysis example found at http://opendata.cern.ch/record/101 is simply 101.

.. code-block:: console

    $ python opendata_analysis_query.py -r 101

The program will then begin querying the provided analysis record and
automatically downloading all of the index files listed within the dataset
links under the **Use With** section of the record. The program provides some
output informing the user of the completion of all the downloads as well as the
name of the directory where these downloads can be found. If the command above
runs successfully, you should see something like this:


.. code-block:: console

    Getting index files for 'Two-lepton/four-lepton analysis example of CMS 2010 open data'...

    Downloaded 1 index files from Electron/Run2010B-Apr21ReReco-v1
    Downloaded 1 index files from Mu/Run2010B-Apr21ReReco-v1

    Query Complete: Downloaded 2 index files to the folder ./rec101_datasets/


Development Notes
=================

Please see comments within the python script (opendata_analysis_query.py)
 for detailed descriptions of what the script does.

The script uses the `Requests <http://docs.python-requests.org/en/master/>`_
python library to send HTTP requests and verify that each request is ok using
the built in raise_for_status() method.
