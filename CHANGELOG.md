<!-- markdownlint-disable MD012 MD013 MD024 -->

# Changelog

## [1.1.0](https://github.com/cernopendata/cernopendata-client/compare/1.0.2...1.1.0) (2025-12-19)


### Features

* **etc:** add bash and zsh shell completion files ([#172](https://github.com/cernopendata/cernopendata-client/issues/172)) ([956ae1e](https://github.com/cernopendata/cernopendata-client/commit/956ae1e92f97db26b821828672b49bf582e66316))


### Documentation

* **usage:** add shell completion instructions ([#172](https://github.com/cernopendata/cernopendata-client/issues/172)) ([b28a25e](https://github.com/cernopendata/cernopendata-client/commit/b28a25e8ac1625e8cbd443d48bce00f621d231fe))

## [1.0.2](https://github.com/cernopendata/cernopendata-client/compare/1.0.1...1.0.2) (2025-12-17)


### Bug fixes

* **download:** use record IDs for all local data paths ([#167](https://github.com/cernopendata/cernopendata-client/issues/167)) ([9b97f7c](https://github.com/cernopendata/cernopendata-client/commit/9b97f7caebf2c049f2734ec1af399c6aeb027341)), closes [#166](https://github.com/cernopendata/cernopendata-client/issues/166)
* **verifier:** zero-pad Adler32 checksums to 8 hex characters ([#169](https://github.com/cernopendata/cernopendata-client/issues/169)) ([b6daa50](https://github.com/cernopendata/cernopendata-client/commit/b6daa508c3d190585f84853687ff0cfb8acbe792))


### Code refactoring

* **searcher:** remove Python 2 compatibility code ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([cc3bb8b](https://github.com/cernopendata/cernopendata-client/commit/cc3bb8b80b6cf383168e0edf93ae17fafe65ab5c))
* **validator:** remove Python 2 compatibility code ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([b03de4f](https://github.com/cernopendata/cernopendata-client/commit/b03de4fb7519864a1e0f1f1380467007c5a73b17))


### Test suite

* **conftest:** add fixture for automatic directory cleanup ([#168](https://github.com/cernopendata/cernopendata-client/issues/168)) ([b847121](https://github.com/cernopendata/cernopendata-client/commit/b84712178cd143d86d66642b09e45d1ffdd9f6b0))
* **conftest:** add shared CLI runner fixture ([#168](https://github.com/cernopendata/cernopendata-client/issues/168)) ([b387fde](https://github.com/cernopendata/cernopendata-client/commit/b387fde1569c7e81c825fe3b8601a4cbefe51fbd))
* **downloader:** add unit tests for file filtering functions ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([a93d2be](https://github.com/cernopendata/cernopendata-client/commit/a93d2be9528016868a06cf0622c13f83493a834d))
* **get-metadata:** add test for filter without output-value ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([7c65a79](https://github.com/cernopendata/cernopendata-client/commit/7c65a79de09b675847067db7c6f036cf0f62588c))
* **global:** add [@pytest](https://github.com/pytest).mark.local marker for local-only tests ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([59fb1da](https://github.com/cernopendata/cernopendata-client/commit/59fb1da2a4ffd6160ad7cd8ce291d88c4774e807))
* **list-directory:** add test for empty directory ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([22e75e5](https://github.com/cernopendata/cernopendata-client/commit/22e75e56cab423905d701a4de05295fcfd319d3d))
* **metadater:** add tests for filter edge cases ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([b1855b9](https://github.com/cernopendata/cernopendata-client/commit/b1855b9e12b1c8365cdcf1c3f6e73227dedbfba6))
* **validator:** correct typos in test assertions ([#170](https://github.com/cernopendata/cernopendata-client/issues/170)) ([07b7b00](https://github.com/cernopendata/cernopendata-client/commit/07b7b00376921288fbb3aed66fac9ce04866858c))


### Continuous integration

* **commitlint:** fix local running of commit linter on macOS ([#168](https://github.com/cernopendata/cernopendata-client/issues/168)) ([6f411b1](https://github.com/cernopendata/cernopendata-client/commit/6f411b1b4ed859b18a54365d43a0f748dbfa7c9c))


### Documentation

* **claude:** add initial Claude Code configuration ([#164](https://github.com/cernopendata/cernopendata-client/issues/164)) ([7d14b38](https://github.com/cernopendata/cernopendata-client/commit/7d14b3845b859af2f2282f565f1c040898adc7f6))
* **claude:** expand file change instructions for all file types ([#168](https://github.com/cernopendata/cernopendata-client/issues/168)) ([5652939](https://github.com/cernopendata/cernopendata-client/commit/5652939b50c1b0dd60471961e80476dcad64ab0a))

## [1.0.1](https://github.com/cernopendata/cernopendata-client/compare/1.0.0...1.0.1) (2025-11-10)


### Build

* **python:** add support for Python 3.14 ([#158](https://github.com/cernopendata/cernopendata-client/issues/158)) ([0083d29](https://github.com/cernopendata/cernopendata-client/commit/0083d290687bc462f97c060b45e3d0a4c6eee131))


### Bug fixes

* **searcher:** respect `get-file-locations --protocol` parameter ([#154](https://github.com/cernopendata/cernopendata-client/issues/154)) ([625eb9d](https://github.com/cernopendata/cernopendata-client/commit/625eb9d301a4a8d3c5fef25efdeb505fe45b846c)), closes [#152](https://github.com/cernopendata/cernopendata-client/issues/152)
* **searcher:** respect `get-file-locations --server` parameter ([#155](https://github.com/cernopendata/cernopendata-client/issues/155)) ([16af0d0](https://github.com/cernopendata/cernopendata-client/commit/16af0d0b90a75c38551b4c152bfad33b4886ed45)), closes [#153](https://github.com/cernopendata/cernopendata-client/issues/153)


### Test suite

* **verifier:** replace `sed` calls with native Python code ([#157](https://github.com/cernopendata/cernopendata-client/issues/157)) ([20588e8](https://github.com/cernopendata/cernopendata-client/commit/20588e8a5dc919476db6d447ec6daed331b18130))

## [1.0.0](https://github.com/cernopendata/cernopendata-client/compare/0.4.0...1.0.0) (2025-02-25)


### ⚠ BREAKING CHANGES

* **python:** Drops support for Python 3.6 and 3.7.

### Build

* **docker:** upgrade to Ubuntu 24.04 and Python 3.12 ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([bac8200](https://github.com/cernopendata/cernopendata-client/commit/bac82006d8ab701c45c4a80df6cec1abfec5963a))
* **python:** add support for Python 3.13 ([#146](https://github.com/cernopendata/cernopendata-client/issues/146)) ([1714dbf](https://github.com/cernopendata/cernopendata-client/commit/1714dbf62fef7a9267629c2baef77d33427c15d0))
* **python:** drop support for Python 3.6 and 3.7 ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([cb633e0](https://github.com/cernopendata/cernopendata-client/commit/cb633e0f3a49484a852033bdf053207b0233670d))


### Bug fixes

* **searcher:** adapt to the new metadata schema with file indices ([#147](https://github.com/cernopendata/cernopendata-client/issues/147)) ([bab9401](https://github.com/cernopendata/cernopendata-client/commit/bab94012690bdd7a71ad2542920a8a82b670ddf3)), closes [#148](https://github.com/cernopendata/cernopendata-client/issues/148)


### Code refactoring

* **docs:** move from reST to Markdown ([#145](https://github.com/cernopendata/cernopendata-client/issues/145)) ([845b1bc](https://github.com/cernopendata/cernopendata-client/commit/845b1bc09d6b022d744bec87e79208d4ce2d0691))


### Test suite

* **metadater:** adapt filtering test after CCID removal ([#147](https://github.com/cernopendata/cernopendata-client/issues/147)) ([4ff86a9](https://github.com/cernopendata/cernopendata-client/commit/4ff86a91d87b57da15b48dfd491ae8913a156567))


### Continuous integration

* **actions:** update GitHub actions due to Node 16 deprecation ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([a3a898e](https://github.com/cernopendata/cernopendata-client/commit/a3a898ed9bd50b30b439b60e90cd166b74615524))
* **actions:** upgrade to Ubuntu 24.04 and Python 3.12 ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([925c0b5](https://github.com/cernopendata/cernopendata-client/commit/925c0b5ddc471bc6937b718f4178934bd818602a))
* **commitlint:** addition of commit message linter ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([e01fff8](https://github.com/cernopendata/cernopendata-client/commit/e01fff80623da66299794dec3f94ec9c1946fbb3))
* **jsonlint:** add JSON linting ([#150](https://github.com/cernopendata/cernopendata-client/issues/150)) ([cab5fcb](https://github.com/cernopendata/cernopendata-client/commit/cab5fcba919557af09b39df7cf99c7390f4b8679))
* **markdownlint:** add Markdown linting ([#150](https://github.com/cernopendata/cernopendata-client/issues/150)) ([45a2a5f](https://github.com/cernopendata/cernopendata-client/commit/45a2a5f6aa5f3f9d64dfcda45e1eec9e67d3515d))
* **prettier:** add Prettier code formatting checks ([#150](https://github.com/cernopendata/cernopendata-client/issues/150)) ([1020c7c](https://github.com/cernopendata/cernopendata-client/commit/1020c7cf5dde9c3397e3073eda73ba0537081351))
* **release-please:** increment version number in Dockerfile ([#151](https://github.com/cernopendata/cernopendata-client/issues/151)) ([1bbfcd5](https://github.com/cernopendata/cernopendata-client/commit/1bbfcd5d1a6fa0f32014e2ad50f3a255b0ca1f55))
* **release-please:** initial Release Please configuration ([#143](https://github.com/cernopendata/cernopendata-client/issues/143)) ([5724844](https://github.com/cernopendata/cernopendata-client/commit/5724844659369e7888a76bf58abf5e556c9f286e))
* **run-tests:** add usage help and refactor options ([#150](https://github.com/cernopendata/cernopendata-client/issues/150)) ([b9368d8](https://github.com/cernopendata/cernopendata-client/commit/b9368d83577bdc1e0a2305dde56c2fc22ff97eb9))
* **run-tests:** stop properly after running all tests ([#145](https://github.com/cernopendata/cernopendata-client/issues/145)) ([357a719](https://github.com/cernopendata/cernopendata-client/commit/357a719b25aa65ce8569989a3abd2c92f0a5e7e9))
* **shfmt:** add shfmt code formatting checks ([#150](https://github.com/cernopendata/cernopendata-client/issues/150)) ([e70291e](https://github.com/cernopendata/cernopendata-client/commit/e70291e62e9331e46977741f847383de32c7f08c))
* **yamllint:** add YAML linting ([#150](https://github.com/cernopendata/cernopendata-client/issues/150)) ([0d70783](https://github.com/cernopendata/cernopendata-client/commit/0d707832ef1835092d043d15e44b01f5dda0730c))


### Documentation

* **usage:** add an example on how to retrieve container images ([#141](https://github.com/cernopendata/cernopendata-client/issues/141)) ([fef3295](https://github.com/cernopendata/cernopendata-client/commit/fef329555565c2d6a4b0841da57b7fe7665c49c5))

## 0.4.0 (2024-08-22)

* Adds support for Python 3.11 and 3.12.
* Improves `get-metadata --output-field` command by adding a new `--filter`
  option allowing to output only selected field values matching desired
  criteria.
* Changes container image base to Fedora 38 and slightly optimises image size.
* Drops support for Python 2.7.

## 0.3.0 (2022-03-16)

* Adds support for Python 3.10.
* Improves `download-files` command to resume interrupted downloads when using
  HTTP downloads with `pycurl` engine.
* Improves XRootD downloader by using vanilla XRootD package. Changes
  `xrootdpyfs` to `xrootd` download engine.
* Improves `download-files` command with a new option `--download-engine` to
  select `pycurl` or `requests` engines when downloading files over HTTP.
* Fixes minor issues with file index unwinding and output directory handling.

## 0.2.0 (2020-11-19)

* Adds new `list-directory` command to list content of EOS directories holding
  open data files.
* Adds support for Python 3.9.
* Improves `download-files` command to allow using XRootD protocol.
* Improves `download-files` command to allow using HTTPS protocol.
* Improves `download-files` command to optionally verify file integrity as soon
  as files are being downloaded.
* Improves `get-file-locations` command to optionally output file sizes and
  checksums.
* Improves output format colouring to better indicate notes and errors.
* Fixes minor issues and improves code coverage.

## 0.1.0 (2020-09-24)

* Enriches `download-files` command to optionally download only files matching
  certain name, regexp, or range count.
* Adds new `verify-files` command to verify number, size, and checksum of
  downloaded files.
* Improves `get-metadata` command with respect to outputting only certain
  desired metadata field values.
* Enriches user documentation.

## 0.0.1 (2020-09-09)

* Initial public release.
