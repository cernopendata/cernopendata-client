.. _usage:

Usage
=====

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
    list-directory      List contents of a EOSPUBLIC Open Data directory.
    verify-files        Verify downloaded data file integrity.
    version             Return cernopendata-client version.

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
        "$schema": "http://opendata.cern.ch/schema/records/record-v1.0.0.json",
        "abstract": {
            "description": "<p>BTau primary dataset in AOD format from RunB of 2010</p> <p>This dataset contains all runs from 2010 RunB. The list of validated runs, which must be applied to all analyses, can be found in</p>",
            "links": [
                {
                    "recid": "1000"
                }
            ]
        },
        "accelerator": "CERN-LHC",
        "collaboration": {
            "name": "CMS collaboration",
            "recid": "450"
        },
    ...

This will output a JSON containing all the record metadata, such as
title, authors, keywords, collision energy, etc. The JSON may also
contain interesting physics information describing the dataset.

If you would like to extract parts of metadata, for example to extract
only the dataset title, or only the Global Tag information for CMS
datasets, you can use **--output-value** command-line option:

.. code-block:: console

    $ cernopendata-client get-metadata --recid 1 --output-value title
    /BTau/Run2010B-Apr21ReReco-v1/AOD
    $ cernopendata-client get-metadata --recid 1 --output-value system_details.global_tag
    FT_R_42_V10A::All

Listing available data files
----------------------------

In order to get a list of data files belonging to a record, please use
the **get-file-locations** command:

**HTTP protocol**

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

This command will output URIs for all the files associated with the record ID
5500, using the HTTP protocol. Note that you can specify ``--server
https://opendata.cern.ch`` if you would like to use the HTTPS protocol instead.

**XRootD protocol**

Note that you can use ``--protocol xrootd`` command-line option if you
would rather see the equivalent XRootD endpoints for the files:

.. code-block:: console

    $ cernopendata-client get-file-locations --recid 5500 --protocol xrootd
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

**File sizes and checksums**

If you would like to know in advance the file sizes and checksums, you can use
``--verbose`` option:

.. code-block:: console

    $ cernopendata-client get-file-locations --recid 5500 --verbose
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/BuildFile.xml	305	adler32:ff63668a
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/HiggsDemoAnalyzer.cc	83761	adler32:f205f068
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/List_indexfile.txt	1669	adler32:46a907fc
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall.cc	14943	adler32:af301992
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/M4Lnormdatall_lvl3.cc	15805	adler32:9d9b2126
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level3MC.py	3741	adler32:cc943381
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level3data.py	3689	adler32:1d3e2a43
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level4MC.py	3874	adler32:9cbd53a3
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/demoanalyzer_cfg_level4data.py	3821	adler32:177b49c0
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/mass4l_combine.pdf	18170	adler32:19c6a6a2
    http://opendata.cern.ch/eos/opendata/cms/software/HiggsExample20112012/mass4l_combine.png	93152	adler32:62e0c299

Downloading data files
----------------------

In order to download data files belonging to a record, please use the
**download-files** command. The command can download files over HTTP, HTTPS or
XRootD protocols and verify the file checksums.

**HTTP protocol**

By default the **download-files** command uses HTTP protocol:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500
    ==> Downloading file 1 of 11
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 KiB (100%)
    ==> Downloading file 2 of 11
      -> File: ./5500/HiggsDemoAnalyzer.cc
      -> Progress: 81/81 KiB (100%)
    ==> Downloading file 3 of 11
      -> File: ./5500/List_indexfile.txt
      -> Progress: 1/1 KiB (100%)
    ==> Downloading file 4 of 11
      -> File: ./5500/M4Lnormdatall.cc
      -> Progress: 14/14 KiB (100%)
    ==> Downloading file 5 of 11
      -> File: ./5500/M4Lnormdatall_lvl3.cc
      -> Progress: 15/15 KiB (100%)
    ==> Downloading file 6 of 11
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 7 of 11
      -> File: ./5500/demoanalyzer_cfg_level3data.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 8 of 11
      -> File: ./5500/demoanalyzer_cfg_level4MC.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 9 of 11
      -> File: ./5500/demoanalyzer_cfg_level4data.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 10 of 11
      -> File: ./5500/mass4l_combine.pdf
      -> Progress: 17/17 KiB (100%)
    ==> Downloading file 11 of 11
      -> File: ./5500/mass4l_combine.png
      -> Progress: 90/90 KiB (100%)
    ==> Success!

The command will download files into a local directory called ``5500`` after
the record ID input parameter.

By default the download will be carried out over HTTP protocol. If you would
like to use the HTTPS protocol instead , please specify ``--server
https://opendata.cern.ch``.

Note that you can also download files from another server, for example from our
Quality Assurance server, by using ``--server http://opendata-qa.cern.ch``.

**XRootD protocol**

If you have installed client with XRootD support, you can use ``--protocol
xrootd`` command-line option to use that protocol instead of HTTP/HTTPS:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --protocol xrootd
    ==> Downloading file 1 of 11
      -> File: ./5500/BuildFile.xml
    ==> Downloading file 2 of 11
      -> File: ./5500/HiggsDemoAnalyzer.cc
    ==> Downloading file 3 of 11
      -> File: ./5500/List_indexfile.txt
    ==> Downloading file 4 of 11
      -> File: ./5500/M4Lnormdatall.cc
    ==> Downloading file 5 of 11
      -> File: ./5500/M4Lnormdatall_lvl3.cc
    ==> Downloading file 6 of 11
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
    ==> Downloading file 7 of 11
      -> File: ./5500/demoanalyzer_cfg_level3data.py
    ==> Downloading file 8 of 11
      -> File: ./5500/demoanalyzer_cfg_level4MC.py
    ==> Downloading file 9 of 11
      -> File: ./5500/demoanalyzer_cfg_level4data.py
    ==> Downloading file 10 of 11
      -> File: ./5500/mass4l_combine.pdf
    ==> Downloading file 11 of 11
      -> File: ./5500/mass4l_combine.png
    ==> Success!

**Select download engine**

You can specify the download engine with ``--download-engine`` option.

- ``requests`` and ``pycurl`` are two supported download engines for **HTTP** protocol.
- ``xrootd`` is the only supported download engine for **XRootD** protocol.

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-name BuildFile.xml --download-engine pycurl
    ==> Downloading file 1 of 1
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 KiB (100%)
    ==> Success!

**Filter by name**

A dataset may consist of thousands of files. You can use powerful filtering
options to download only certain files matching your criteria.

For example, you can download only files matching exactly a given file name using the ``--filter-name`` option:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-name BuildFile.xml
    ==> Downloading file 1 of 1
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 KiB (100%)
    ==> Success!

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-name BuildFile.xml,List_indexfile.txt
    ==> Downloading file 1 of 2
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 KiB (100%)
    ==> Downloading file 2 of 2
      -> File: ./5500/List_indexfile.txt
      -> Progress: 1/1 KiB (100%)
    ==> Success!

**Filter by regular expression**

You can download all files matching a certain regular expression using the ``--filter-regexp`` option:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-regexp py$
    ==> Downloading file 1 of 4
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 2 of 4
      -> File: ./5500/demoanalyzer_cfg_level3data.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 3 of 4
      -> File: ./5500/demoanalyzer_cfg_level4MC.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 4 of 4
      -> File: ./5500/demoanalyzer_cfg_level4data.py
      -> Progress: 3/3 KiB (100%)
    ==> Success!

**Filter by range**

You can also download files from a specified range (i-j) using the ``--filter-range`` option:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-range 1-4
    ==> Downloading file 1 of 4
      -> File: ./5500/BuildFile.xml
      -> Progress: 0/0 KiB (100%)
    ==> Downloading file 2 of 4
      -> File: ./5500/HiggsDemoAnalyzer.cc
      -> Progress: 81/81 KiB (100%)
    ==> Downloading file 3 of 4
      -> File: ./5500/List_indexfile.txt
      -> Progress: 1/1 KiB (100%)
    ==> Downloading file 4 of 4
      -> File: ./5500/M4Lnormdatall.cc
      -> Progress: 14/14 KiB (100%)
    ==> Success!

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-range 1-2,5-7
    ==> Downloading file 1 of 5
      -> File: ./5500/BuildFile.xml
    ==> Downloading file 2 of 5
      -> File: ./5500/HiggsDemoAnalyzer.cc
    ==> Downloading file 3 of 5
      -> File: ./5500/M4Lnormdatall_lvl3.cc
    ==> Downloading file 4 of 5
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
    ==> Downloading file 5 of 5
      -> File: ./5500/demoanalyzer_cfg_level3data.py
    ==> Success!

**Filter by combining multiple selectors**

You can combine multiple filters in the same download command. Here are several
examples:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range 1-2
    ==> Downloading file 1 of 2
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
      -> Progress: 3/3 KiB (100%)
    ==> Downloading file 2 of 2
      -> File: ./5500/demoanalyzer_cfg_level3data.py
      -> Progress: 3/3 KiB (100%)
    ==> Success!

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-regexp py --filter-range 1-2,4-4
    ==> Downloading file 1 of 3
      -> File: ./5500/demoanalyzer_cfg_level3MC.py
    ==> Downloading file 2 of 3
      -> File: ./5500/demoanalyzer_cfg_level3data.py
    ==> Downloading file 3 of 3
      -> File: ./5500/demoanalyzer_cfg_level4data.py
    ==> Success!

Verifying files
---------------

If you have downloaded the data files for a certain record, and you would like
to verify their integrity and check whether there haven't been some critical
updates on the CERN Open Data portal side, you can use the **verify-files**
command:

.. code-block:: console

    $ cernopendata-client verify-files --recid 5500
    ==> Verifying number of files for record 5500...
      -> Expected 11, found 11
    ==> Verifying file BuildFile.xml...
      -> Expected size 305, found 305
      -> Expected checksum adler32:ff63668a, found adler32:ff63668a
    ==> Verifying file HiggsDemoAnalyzer.cc...
      -> Expected size 83761, found 83761
      -> Expected checksum adler32:f205f068, found adler32:f205f068
    ==> Verifying file List_indexfile.txt...
      -> Expected size 1669, found 1669
      -> Expected checksum adler32:46a907fc, found adler32:46a907fc
    ==> Verifying file M4Lnormdatall.cc...
      -> Expected size 14943, found 14943
      -> Expected checksum adler32:af301992, found adler32:af301992
    ==> Verifying file M4Lnormdatall_lvl3.cc...
      -> Expected size 15805, found 15805
      -> Expected checksum adler32:9d9b2126, found adler32:9d9b2126
    ==> Verifying file demoanalyzer_cfg_level3MC.py...
      -> Expected size 3741, found 3741
      -> Expected checksum adler32:cc943381, found adler32:cc943381
    ==> Verifying file demoanalyzer_cfg_level3data.py...
      -> Expected size 3689, found 3689
      -> Expected checksum adler32:1d3e2a43, found adler32:1d3e2a43
    ==> Verifying file demoanalyzer_cfg_level4MC.py...
      -> Expected size 3874, found 3874
      -> Expected checksum adler32:9cbd53a3, found adler32:9cbd53a3
    ==> Verifying file demoanalyzer_cfg_level4data.py...
      -> Expected size 3821, found 3821
      -> Expected checksum adler32:177b49c0, found adler32:177b49c0
    ==> Verifying file mass4l_combine.pdf...
      -> Expected size 18170, found 18170
      -> Expected checksum adler32:19c6a6a2, found adler32:19c6a6a2
    ==> Verifying file mass4l_combine.png...
      -> Expected size 93152, found 93152
      -> Expected checksum adler32:62e0c299, found adler32:62e0c299
    ==> Success!

Note that you can verify each file "just in time" as it is being downloaded as well:

.. code-block:: console

    $ cernopendata-client download-files --recid 5500 --filter-range 1-4 --verify
    ==> Downloading file 1 of 4
      -> File: ./5500/BuildFile.xml
    ==> Verifying file BuildFile.xml...
      -> Expected size 305, found 305
      -> Expected checksum adler32:ff63668a, found adler32:ff63668a
    ==> Downloading file 2 of 4
      -> File: ./5500/HiggsDemoAnalyzer.cc
    ==> Verifying file HiggsDemoAnalyzer.cc...
      -> Expected size 83761, found 83761
      -> Expected checksum adler32:f205f068, found adler32:f205f068
    ==> Downloading file 3 of 4
      -> File: ./5500/List_indexfile.txt
    ==> Verifying file List_indexfile.txt...
      -> Expected size 1669, found 1669
      -> Expected checksum adler32:46a907fc, found adler32:46a907fc
    ==> Downloading file 4 of 4
      -> File: ./5500/M4Lnormdatall.cc
    ==> Verifying file M4Lnormdatall.cc...
      -> Expected size 14943, found 14943
      -> Expected checksum adler32:af301992, found adler32:af301992
    ==> Success!

Listing directories
-------------------

The CERN Open Data files are hosted on the EOSPUBLIC data storage service.
In order to get a list of files belonging to a certain EOSPUBLIC directory, please use
the **list-directory** command:

.. code-block:: console

    $ cernopendata-client list-directory /eos/opendata/cms/validated-runs/Commissioning10
    Commissioning10-May19ReReco_7TeV.json
    Commissioning10-May19ReReco_900GeV.json

The **list-directory** command uses XRootD protocol to list data files and
hence it is available only when you install the XRootD flavour. Please see the
:ref:`installation` documentation for more details.

**Iterate recursively**

Note that you can use ``--recursive`` command-line option if you would like to
iterate also through all the subdirectories of the given directory:

.. code-block:: console

    $ cernopendata-client list-directory /eos/opendata/cms/validated-runs --recursive
    Commissioning10-May19ReReco_7TeV.json
    Commissioning10-May19ReReco_900GeV.json
    Cert_190456-208686_8TeV_22Jan2013ReReco_Collisions12_JSON.txt
    Cert_160404-180252_7TeV_ReRecoNov08_Collisions11_JSON.txt
    Cert_136033-149442_7TeV_Apr21ReReco_Collisions10_JSON_v2.txt

**Iterate recursively with timeout**

If you would like to list a directory that contains a large amount of files,
you can specify ``--timeout`` option in order to exit after a certain amount of
time. The default timeout is 60 seconds.

.. code-block:: console

    $ cernopendata-client list-directory /eos/opendata/cms/Run2010B/BTau/AOD --recursive --timeout 30
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0000_file_index.json
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0000_file_index.txt
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0001_file_index.json
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0001_file_index.txt
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0002_file_index.json
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0002_file_index.txt
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0003_file_index.json
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0003_file_index.txt
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0004_file_index.json
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0004_file_index.txt
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0005_file_index.json
    CMS_Run2010B_BTau_AOD_Apr21ReReco-v1_0005_file_index.txt
    ..

More information
----------------

For more information about all the available ``cernopendata-client`` commands
and options, please see :ref:`cliapi`.
