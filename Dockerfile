# This file is part of cernopendata-client.
#
# Copyright (C) 2020 CERN.
#
# cernopendata-client is free software; you can redistribute it and/or modify
# it under the terms of the GPLv3 license; see LICENSE file for more details.

# Use Python 3.8 slim base image
FROM python:3.8-slim

# Install system prerequisites
RUN apt-get update -y && \
    apt-get install -y \
        curl \
        gcc \
        libcurl4-openssl-dev \
        libssl-dev && \
    apt-get autoremove && \
    apt-get clean

# Add sources to `/code` and work there
WORKDIR /code
ADD . /code

# Install cernopendata-client
RUN pip install .

# Remove /code to make image slimmer
RUN rm -rf /code

# Run container as `cernopendata` user with UID `1000`, which should match
# current host user in most situations
RUN adduser --uid 1000 --disabled-password --gecos '' cernopendata

# Run cernopendata-client upon entry
USER cernopendata
ENTRYPOINT ["cernopendata-client"]
