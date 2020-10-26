# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

# Use CentOS8
FROM centos:8

# Install system prerequisites
RUN yum update -y && \
    yum install -y \
        ca-certificates \
        epel-release && \
    yum groupinstall -y "Development Tools" && \
    yum install -y \
        cmake \
        curl \
        gcc \
        gcc-c++ \
        python3 \
        python3-pip \
        python3-devel \
        libcurl-devel \
        zlib-devel \
        libuuid-devel \
        openssl-devel && \
    yum autoremove && \
    yum clean all

# Install some prerequisites ahead of `setup.py` in order to take advantage of
# the docker build cache:
RUN pip3 install --upgrade pip setuptools
RUN pip3 install wheel

# Add sources to `/code` and work there
WORKDIR /code
ADD . /code

# Install cernopendata-client
RUN pip3 install .[xroot]

# Remove /code to make image slimmer
RUN rm -rf /code

# Run container as `cernopendata` user with UID `1000`, which should match
# current host user in most situations
RUN adduser --uid 1000  cernopendata --gid 0 && \
    chown -R  cernopendata:root /code

# Run cernopendata-client upon entry
USER cernopendata
ENTRYPOINT ["cernopendata-client"]
