# CLAUDE.md

This file provides guidance for Claude Code when working with this repository.

## Project Overview

`cernopendata-client` is a command-line tool to download files from the CERN
Open Data portal. It enables querying datasets and downloading/verifying
individual data files.

## Development Setup

```bash
# Using mise (recommended) - installs Python versions 3.8-3.14
mise install

# Create virtual environment and install in editable mode
python3 -m venv env
source env/bin/activate
pip install -e '.[tests]'
```

## Testing and Code Quality

The project uses `run-tests.sh` for all quality checks. Run all checks with:

```bash
./run-tests.sh
```

### Individual Check Commands

| Command                              | Description                            |
| ------------------------------------ | -------------------------------------- |
| `./run-tests.sh --python-tests`      | Run pytest test suite                  |
| `./run-tests.sh --format-black`      | Check Python formatting (black)        |
| `./run-tests.sh --lint-flake8`       | Lint Python code (flake8)              |
| `./run-tests.sh --lint-pydocstyle`   | Check Python docstrings                |
| `./run-tests.sh --format-prettier`   | Check Markdown/YAML formatting         |
| `./run-tests.sh --format-shfmt`      | Check shell script formatting          |
| `./run-tests.sh --lint-shellcheck`   | Lint shell scripts                     |
| `./run-tests.sh --lint-markdownlint` | Lint Markdown files                    |
| `./run-tests.sh --lint-yamllint`     | Lint YAML files                        |
| `./run-tests.sh --lint-jsonlint`     | Lint JSON files                        |
| `./run-tests.sh --lint-commitlint`   | Check commit message format            |
| `./run-tests.sh --lint-manifest`     | Check Python manifest (check-manifest) |
| `./run-tests.sh --docs-sphinx`       | Build and test Sphinx documentation    |
| `./run-tests.sh --docker-build`      | Build Docker image                     |
| `./run-tests.sh --docker-tests`      | Run tests in Docker container          |
| `./run-tests.sh --lint-hadolint`     | Lint Dockerfile                        |

### Using tox for Multi-Python Testing

```bash
tox           # Run tests across all Python versions (3.8-3.14)
tox -e py312  # Run tests for specific Python version
```

## Project Structure

- `cernopendata_client/` - Main Python package
  - `cli.py` - Command-line interface (Click-based)
  - `downloader.py` - File download functionality
  - `searcher.py` - Dataset search functionality
  - `verifier.py` - File verification
  - `validator.py` - Input validation
  - `metadater.py` - Metadata handling
  - `config.py` - Configuration
  - `printer.py` - Output formatting
  - `utils.py` - Utility functions
  - `walker.py` - Directory traversal
- `tests/` - Test suite
- `docs/` - Sphinx documentation

## Code Style

- Python formatting: black
- Python linting: flake8
- Docstrings: pydocstyle (ignores D413, D301)
- Commit messages: conventional commits (commitlint)
- Shell scripts: shellcheck + shfmt
- Markdown/YAML/JSON: prettier + markdownlint + yamllint + jsonlint

## Key Notes

- License: GPLv3
- Python support: 3.8 - 3.14
- Main branch: `master`
