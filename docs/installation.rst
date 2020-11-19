.. _installation:

Installation
============

PyPI
----

``cernopendata-client`` is available on PyPI. You can install it into your
personal user space by doing:

.. code-block:: console

   $ pip install --user cernopendata-client

You can also install it into a new virtual environment:

.. code-block:: console

   $ virtualenv ~/.virtualenvs/cernopendata-client
   $ source ~/.virtualenvs/cernopendata-client/bin/activate
   $ pip install cernopendata-client

If you would like to use a more performing **pycurl** library for downloading
data, please add the `pycurl` flavour while installing the client. Note that
you need to have `curl <https://curl.se/>`_ and `openssl
<https://www.openssl.org/>`_ set up on your system:

.. code-block:: console

   $ pip install cernopendata-client[pycurl]

Additionally, if you would like to use the powerful **XRootD** protocol for
downloading data, please add the `xrootd` flavour when installing the client.
Note that you would need to have `xrootd <https://xrootd.slac.stanford.edu/>`_
set up on your system:

.. code-block:: console

   $ pip install cernopendata-client[xrootd]

Finally, note that you can combine both flavours, if you wish to have both
capabilities:

.. code-block:: console

   $ pip install cernopendata-client[pycurl,xrootd]

Docker
------

If you would like to use ``cernopendata-client`` as a standalone Docker
container, you can pull and use the client image as follows. Note that the
image contains both `pycurl` and `xrootd` flavours:

.. code-block:: console

   $ docker pull cernopendata/cernopendata-client
   $ docker run -i -t --rm cernopendata/cernopendata-client --help

