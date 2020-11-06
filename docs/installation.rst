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

If you would like to use a more performing **pycurl** library for downloading data, please add the `pycurl` flavour while installing `cernopendata-client`:

.. code-block:: console

   $ pip install cernopendata-client[pycurl]

Note that you need to have `curl <https://curl.se/>`_ and `openssl <https://www.openssl.org/>`_ set up on your system.

Additionally, if you want to use an even more powerful **XRootD** protocol for downloading data, please add the `xrootd` flavour when installing `cernopendata-client`:

.. code-block:: console

   $ pip install cernopendata-client[xrootd]

Note that you need to have `xrootd <https://xrootd.slac.stanford.edu/>`_ set up on your system.

Finally, note that you can combine both flavours, if you wish to have both capabilities:

.. code-block:: console

   $ pip install cernopendata-client[pycurl,xrootd]

Docker
------

If you would like to use ``cernopendata-client`` as a standalone Docker
container, you can pull an image as follows:

.. code-block:: console

   $ docker pull cernopendata/cernopendata-client
