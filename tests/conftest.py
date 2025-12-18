# -*- coding: utf-8 -*-
#
# This file is part of cernopendata-client.
#
# Copyright (C) 2025 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

"""Pytest configuration and shared fixtures."""

import os
import shutil

import pytest
from click.testing import CliRunner


@pytest.fixture(autouse=True)
def cleanup_download_directories():
    """Clean up test download directories before and after each test."""
    # Directories that may be created during tests
    test_dirs = ["3005", "5500", "461", "None"]

    # Cleanup before test
    for test_dir in test_dirs:
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)

    yield

    # Cleanup after test
    for test_dir in test_dirs:
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)


@pytest.fixture
def cli_runner():
    """Provide a Click CLI test runner."""
    return CliRunner()
