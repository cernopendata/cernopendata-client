# This file is part of cernopendata-client.
#
# Copyright (C) 2020, 2022, 2023, 2024 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

# Use Ubuntu LTS base image
FROM docker.io/library/ubuntu:24.04

# Use default answers in installation commands
ENV DEBIAN_FRONTEND=noninteractive

# Allow pip to install packages in the system site-packages dir
ENV PIP_BREAK_SYSTEM_PACKAGES=true

# Install prerequisites
# hadolint ignore=DL3008,DL3013
RUN apt-get update -y && \
    apt-get install --no-install-recommends -y \
      black \
      ca-certificates \
      check-manifest \
      curl \
      libpython3.12 \
      python3-pip \
      python3.12 \
      python3.12-dev \
      python3-certifi \
      python3-click \
      python3-coverage \
      python3-docutils \
      python3-execnet \
      python3-jinja2 \
      python3-mock \
      python3-pbr \
      python3-pip \
      python3-pycurl \
      python3-pydocstyle \
      python3-pytest \
      python3-pytest-cov \
      python3-pytest-mock \
      python3-requests \
      python3-urllib3 \
      python3-wheel \
      python3-xrootd \
      xrootd-client && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add sources to `/code` and work there
WORKDIR /code
COPY . /code

# Install cernopendata-client
# hadolint ignore=DL3013
RUN pip3 install --no-cache-dir '.[pycurl,tests,xrootd]' && \
    rm -rf /code

# Run container as `ubuntu` user with UID `1000`, which should match
# current host user in most situations
RUN chown -R ubuntu /code
USER ubuntu

# Run cernopendata-client upon entry
ENTRYPOINT ["cernopendata-client"]

# Set image labels
LABEL org.opencontainers.image.authors="opendata-team@cern.ch"
LABEL org.opencontainers.image.created="2025-02-25"
LABEL org.opencontainers.image.description="CERN Open Data - command-line client"
LABEL org.opencontainers.image.documentation="https://cernopendata-client.readthedocs.io/"
LABEL org.opencontainers.image.licenses="GPLv3"
LABEL org.opencontainers.image.source="https://github.com/cernopendata/cernopendata-client"
LABEL org.opencontainers.image.title="cernopendata-client"
LABEL org.opencontainers.image.url="https://github.com/cernopendata/cernopendata-client"
LABEL org.opencontainers.image.vendor="cernopendata"
# x-release-please-start-version
LABEL org.opencontainers.image.version="1.0.0"
# x-release-please-end
