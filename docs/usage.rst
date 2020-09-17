.. _gettingstarted:

Usage
=====

General help
------------

In order to get help for any ``cernopendata-client`` command, use the
``--help`` option:

.. code-block:: console

    $ cernopendata-client --help

Selecting records
-----------------

The data published on the `CERN Open Data portal
<http://opendata.cern.ch>`_ are organised in bibliographic
records. Each record is uniquely identified by a numerical **record
ID**, for example `record 1
<http://opendata.cern.ch/record/1>`_. Moreover, some records are
minted with a **Digital Object Identifier (DOI)**, for example
`10.7483/OPENDATA.CMS.A342.9982
<http://doi.org/10.7483/OPENDATA.CMS.A342.9982>`_.  Each of these
identifiers can be used in various ``cernopendata-client`` commands to
select record one is interested at. For example:

.. code-block:: console

    $ cernopendata-client <command> --recid 1
    $ cernopendata-client <command> --doi 10.7483/OPENDATA.CMS.A342.9982

Various available commands are shown below.

Getting metadata
----------------

In order to get metadata information about a record, please use the
**get-metadata** command:

.. code-block:: console

    $ cernopendata-client get-metadata --recid 1
    {
	"created": "2020-08-27T00:39:40.879546+00:00",
	"id": 1,
	"links": {
	    "bucket": "http://opendata.cern.ch/api/files/09e99f71-ed58-4314-af55-7b28149f0861",
	    "self": "http://opendata.cern.ch/api/records/1"
	},
	"metadata": {
	    "$schema": "http://opendata.cern.ch/schema/records/record-v1.0.0.json",
    ...

This will output a JSON containing all the record metadata, such as
title, authors, keywords, collision energy, etc. The JSON may also
contain interesting physics information describing the dataset.

If you would like to extract parts of metadata, for example to extract
only the dataset title, or only the Global Tag information for CMS
datasets, you can pipe the output with suitable command-line tools
such as **jq**:

.. code-block:: console

    $ cernopendata-client get-metadata --recid 1 | jq -S '.metadata.title'
    "/BTau/Run2010B-Apr21ReReco-v1/AOD"
    $ cernopendata-client get-metadata --recid 1 | jq -S '.metadata.system_details.global_tag'
    "FT_R_42_V10A::All"

Listing available data files
----------------------------

**HTTP protocol**

In order to get a list of data files belonging to a record, please use
the **get-file-locations** command:

.. code-block:: console

    $ cernopendata-client get-file-locations --recid 5500
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/BuildFile.xml
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/HiggsDemoAnalyzer.cc
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/List_indexfile.txt
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall.cc
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall_lvl3.cc
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level3MC.py
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level3data.py
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level4MC.py
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level4data.py
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/mass4l_combine.pdf
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/mass4l_combine.png

This command will output URIs for all the files associated with the record ID 550, using the HTTP protocol.

**XRootD protocol**

Note that you can use ``--protocol root`` command-line option if you
would rather see the equivalent XRootD endpoints for the files:

.. code-block:: console

    $ cernopendata-client get-file-locations --recid 5500 --protocol root
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/BuildFile.xml
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/HiggsDemoAnalyzer.cc
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/List_indexfile.txt
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall.cc
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall_lvl3.cc
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level3MC.py
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level3data.py
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level4MC.py
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level4data.py
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/mass4l_combine.pdf
    root://eospublic.cern.ch//eos/opendata/cms/software/HiggsExample20112012/mass4l_combine.png

The data files can be downloaded via XRootD protocol using the **xrdcp** command.

Downloading data files
----------------------

In order to download data files belonging to a record, please use the
**download-files** command:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500
    ==> Downloading file 1 of 11
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 kiB (100%)

    ==> Downloading file 2 of 11
      -> File: ./5500/HiggsDemoAnalyzer.cc
      -> Progress: 81/81 kiB (100%)

    ==> Downloading file 3 of 11
      -> File: ./5500/List_indexfile.txt
      -> Progress: 1/1 kiB (100%)

    ==> Downloading file 4 of 11
      -> File: ./5500/M4Lnormdatall.cc
      -> Progress: 14/14 kiB (100%)

    ==> Downloading file 5 of 11
      -> File: ./5500/M4Lnormdatall_lvl3.cc
      -> Progress: 15/15 kiB (100%)

    ==> Downloading file 6 of 11
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 7 of 11
      -> File: ./5500/demoanalyzer_cfg_level3data.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 8 of 11
      -> File: ./5500/demoanalyzer_cfg_level4MC.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 9 of 11
      -> File: ./5500/demoanalyzer_cfg_level4data.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 10 of 11
      -> File: ./5500/mass4l_combine.pdf
      -> Progress: 17/17 kiB (100%)

    ==> Downloading file 11 of 11
      -> File: ./5500/mass4l_combine.png
      -> Progress: 90/90 kiB (100%)

    ==> Success!

The command will download files into a `5500` directory.

**Filter by name**

We can download a file matching exactly the file name by the **filter-name** option.

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-name BuildFile.xml
    ==> Downloading file 1 of 1: ./5500/BuildFile.xml
    Download completed!

**Filter by regular expression**

We can download files matching a regular expression by the **filter-regexp** option.

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-regexp py$
    ==> Downloading file 1 of 4
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 2 of 4
      -> File: ./5500/demoanalyzer_cfg_level3data.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 3 of 4
      -> File: ./5500/demoanalyzer_cfg_level4MC.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 4 of 4
      -> File: ./5500/demoanalyzer_cfg_level4data.py
      -> Progress: 3/3 kiB (100%)

    ==> Success!

**Filter by range**

We can download files from a specified list range (i-j) by the **filter-range** option.

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-range 1-4
    ==> Downloading file 1 of 4
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 kiB (100%)

    ==> Downloading file 2 of 4
      -> File: ./5500/HiggsDemoAnalyzer.cc
      -> Progress: 81/81 kiB (100%)

    ==> Downloading file 3 of 4
      -> File: ./5500/List_indexfile.txt
      -> Progress: 1/1 kiB (100%)

    ==> Downloading file 4 of 4
      -> File: ./5500/M4Lnormdatall.cc
      -> Progress: 14/14 kiB (100%)

    ==> Success!

**Filter by multiple options**

We can download files by filtering out with multiple filters.

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range 1-2
    ==> Downloading file 1 of 2
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
      -> Progress: 3/3 kiB (100%)

    ==> Downloading file 2 of 2
      -> File: ./5500/demoanalyzer_cfg_level3data.py
      -> Progress: 3/3 kiB (100%)

    ==> Success!


More information
----------------

For more information about all the available ``cernopendata-client``
commands and options, please see :ref:`cliapi`.
