# Changelog

## [1.0.0](https://github.com/cernopendata/cernopendata-client/compare/0.4.0...1.0.0) (2024-08-29)


### ⚠ BREAKING CHANGES

* **python:** Drops support for Python 3.6 and 3.7.

### Build

* **docker:** upgrade to Ubuntu 24.04 and Python 3.12 ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([bac8200](https://github.com/cernopendata/cernopendata-client/commit/bac82006d8ab701c45c4a80df6cec1abfec5963a))
* **python:** drop support for Python 3.6 and 3.7 ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([cb633e0](https://github.com/cernopendata/cernopendata-client/commit/cb633e0f3a49484a852033bdf053207b0233670d))


### Code refactoring

* **docs:** move from reST to Markdown ([#145](https://github.com/cernopendata/cernopendata-client/issues/145)) ([845b1bc](https://github.com/cernopendata/cernopendata-client/commit/845b1bc09d6b022d744bec87e79208d4ce2d0691))


### Continuous integration

* **actions:** update GitHub actions due to Node 16 deprecation ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([a3a898e](https://github.com/cernopendata/cernopendata-client/commit/a3a898ed9bd50b30b439b60e90cd166b74615524))
* **actions:** upgrade to Ubuntu 24.04 and Python 3.12 ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([925c0b5](https://github.com/cernopendata/cernopendata-client/commit/925c0b5ddc471bc6937b718f4178934bd818602a))
* **commitlint:** addition of commit message linter ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([e01fff8](https://github.com/cernopendata/cernopendata-client/commit/e01fff80623da66299794dec3f94ec9c1946fbb3))
* **release-please:** initial Release Please configuration ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([5724844](https://github.com/cernopendata/cernopendata-client/commit/5724844659369e7888a76bf58abf5e556c9f286e))
* **run-tests:** stop properly after running all tests ([#145](https://github.com/cernopendata/cernopendata-client/issues/145)) ([357a719](https://github.com/cernopendata/cernopendata-client/commit/357a719b25aa65ce8569989a3abd2c92f0a5e7e9))

## 0.4.0 (2024-08-22)

- Adds support for Python 3.11 and 3.12.
- Improves ``get-metadata --output-field`` command by adding a new ``--filter`` option allowing to output only selected field values matching desired criteria.
- Changes container image base to Fedora 38 and slightly optimises image size.
- Drops support for Python 2.7.

## 0.3.0 (2022-03-16)

- Adds support for Python 3.10.
- Improves ``download-files`` command to resume interrupted downloads when
  using HTTP downloads with ``pycurl`` engine.
- Improves XRootD downloader by using vanilla XRootD package. Changes
  ``xrootdpyfs`` to ``xrootd`` download engine.
- Improves ``download-files`` command with a new option ``--download-engine``
  to select ``pycurl`` or ``requests`` engines when downloading files over
  HTTP.
- Fixes minor issues with file index unwinding and output directory handling.

## 0.2.0 (2020-11-19)

- Adds new ``list-directory`` command to list content of EOS directories
  holding open data files.
- Adds support for Python 3.9.
- Improves ``download-files`` command to allow using XRootD protocol.
- Improves ``download-files`` command to allow using HTTPS protocol.
- Improves ``download-files`` command to optionally verify file integrity as
  soon as files are being downloaded.
- Improves ``get-file-locations`` command to optionally output file sizes and
  checksums.
- Improves output format colouring to better indicate notes and errors.
- Fixes minor issues and improves code coverage.

## 0.1.0 (2020-09-24)

- Enriches ``download-files`` command to optionally download only files
  matching certain name, regexp, or range count.
- Adds new ``verify-files`` command to verify number, size, and checksum of
  downloaded files.
- Improves ``get-metadata`` command with respect to outputting only
  certain desired metadata field values.
- Enriches user documentation.

## 0.0.1 (2020-09-09)

- Initial public release.
