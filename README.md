# cernopendata-client

[![image](https://img.shields.io/pypi/pyversions/cernopendata-client.svg)](https://pypi.org/pypi/cernopendata-client)
[![image](https://github.com/cernopendata/cernopendata-client/workflows/CI/badge.svg)](https://github.com/cernopendata/cernopendata-client/actions)
[![image](https://readthedocs.org/projects/cernopendata-client/badge/?version=latest)](https://cernopendata-client.readthedocs.io/en/latest/?badge=latest)
[![image](https://codecov.io/gh/cernopendata/cernopendata-client/branch/master/graph/badge.svg)](https://codecov.io/gh/cernopendata/cernopendata-client)
[![image](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/cernopendata/opendata.cern.ch?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![image](https://img.shields.io/github/license/cernopendata/cernopendata-client.svg)](https://github.com/cernopendata/cernopendata-client/blob/master/LICENSE)

## About

`cernopendata-client` is a command-line tool to facilitate downloading files
from the [CERN Open Data portal](http://opendata.cern.ch/). The tool enables to
query datasets hosted on the CERN Open Data portal and to download and verify
the individual data set files.

## Installation

```console
$ pip install cernopendata-client
```

## Usage

The detailed information on how to install and use `cernopendata-client` can be
found in
[cernopendata-client.readthedocs.io](https://cernopendata-client.readthedocs.io/en/latest/).

## Development

1. Clone the repository:

   ``` console
   $ git clone https://github.com/cernopendata/cernopendata-client
   ```

2. Setup a [virtual environment](https://docs.python.org/3/library/venv.html):

   ``` console
   $ python3 -m venv env
   $ source env/bin/activate
   ```

3. Install [cernopendata-client]{.title-ref} in [editable
   mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html):

   ```console
   $ pip install -e '.[tests]'
   ```

## Useful links

- [CERN Open Data portal](http://opendata.cern.ch/)
- [CERN Open Data user forum](https://opendata-forum.cern.ch/)
