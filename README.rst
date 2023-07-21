###################
cernopendata-client
###################

.. image:: https://img.shields.io/pypi/pyversions/cernopendata-client.svg
   :target: https://pypi.org/pypi/cernopendata-client

.. image:: https://github.com/cernopendata/cernopendata-client/workflows/CI/badge.svg
   :target: https://github.com/cernopendata/cernopendata-client/actions

.. image:: https://readthedocs.org/projects/cernopendata-client/badge/?version=latest
   :target: https://cernopendata-client.readthedocs.io/en/latest/?badge=latest

.. image:: https://codecov.io/gh/cernopendata/cernopendata-client/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/cernopendata/cernopendata-client

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/cernopendata/opendata.cern.ch?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://img.shields.io/github/license/cernopendata/cernopendata-client.svg
   :target: https://github.com/cernopendata/cernopendata-client/blob/master/LICENSE

About
=====

``cernopendata-client`` is a command-line tool to facilitate downloading files
from the `CERN Open Data portal <http://opendata.cern.ch/>`_. The tool enables
to query datasets hosted on the CERN Open Data portal and to download and
verify the individual data set files.

Installation
============

.. code-block:: console

    $ pip install cernopendata-client

Development
============

Once you've completed the below setup, you can proceed to code enhancements
and modifications within the package.

- Clone the github repository.

.. code-block:: console

    $ git clone https://github.com/cernopendata/cernopendata-client.git

- Setup a `virtual environment <https://docs.python.org/3/library/venv.html>`_.

.. code-block:: console

    $ python3 -m venv env
    $ source env/bin/activate

- Install package in `editable mode <https://setuptools.pypa.io/en/latest/userguide/development_mode.html>`_.

.. code-block:: console

    $ pip install -e .

Usage
=====

The detailed information on how to install and use `cernopendata-client` can be
found in `cernopendata-client.readthedocs.io
<https://cernopendata-client.readthedocs.io/en/latest/>`_.

Useful links
============

- `CERN Open Data portal <http://opendata.cern.ch/>`_
- `CERN Open Data user forum <https://opendata-forum.cern.ch/>`_
