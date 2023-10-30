# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2022, 2023 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

# Use Fedora 38
FROM registry.fedoraproject.org/fedora:38

# Install prerequisites
# hadolint ignore=DL3033,DL3041
RUN dnf install -y \
        black \
        ca-certificates \
        check-manifest \
        curl \
        python3-certifi \
        python3-click \
        python3-coverage \
        python3-docutils \
        python3-jinja2 \
        python3-mock \
        python3-pbr \
        python3-pip \
        python3-pycurl \
        python3-pydocstyle \
        python3-pytest \
        python3-pytest-cache \
        python3-pytest-cov \
        python3-pytest-mock \
        python3-requests \
        python3-urllib3 \
        python3-wheel \
        python3-xrootd \
        xrootd-client && \
    dnf autoremove -y && \
    dnf clean all && \
    rm -rf /var/lib/apt/lists/*

# Add sources to `/code` and work there
WORKDIR /code
COPY . /code

# Install cernopendata-client
# hadolint ignore=DL3013
RUN pip3 install --no-cache-dir '.[pycurl,tests,xrootd]' && \
    rm -rf /code

# Run container as `cernopendata` user with UID `1000`, which should match
# current host user in most situations
# hadolint ignore=DL3059
RUN adduser --uid 1000  cernopendata --gid 0 && \
    chown -R  cernopendata:root /code

# Run cernopendata-client upon entry
USER cernopendata
ENTRYPOINT ["cernopendata-client"]
