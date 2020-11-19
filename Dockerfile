# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

# Use CentOS 8.2.2004
FROM centos:8.2.2004

# Install system prerequisites
# hadolint ignore=DL3033
RUN yum install -y \
        ca-certificates \
        epel-release && \
    yum install -y \
        cmake \
        curl \
        gcc \
        gcc-c++ \
        libcurl-devel \
        libuuid-devel \
        make \
        openssl-devel \
        python3-devel \
        python3-pip \
        python3-wheel \
        xrootd-client \
        zlib-devel && \
    yum autoremove && \
    yum clean all

# Add sources to `/code` and work there
WORKDIR /code
COPY . /code

# Install cernopendata-client
# hadolint ignore=DL3013
RUN pip3 install --no-cache-dir '.[all]'

# Remove /code to make image slimmer
RUN rm -rf /code

# Run container as `cernopendata` user with UID `1000`, which should match
# current host user in most situations
RUN adduser --uid 1000  cernopendata --gid 0 && \
    chown -R  cernopendata:root /code

# Run cernopendata-client upon entry
USER cernopendata
ENTRYPOINT ["cernopendata-client"]
