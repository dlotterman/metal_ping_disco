#!/bin/bash

# This is primarily intended to allow the data runner to be run as a cronjob
export METAL_PING_DISCO_AWS_S3_BUCKET="" && \
export METAL_PING_DISCO_AWS_ACCESS_KEY_ID="" && \
export METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY="" && \
export METAL_PING_DISCO_MYSQL_ENDPOINTS_RAW="" && \
export METAL_PING_DISCO_AWS_S3_ENDPOINT=""

source $CHECKOUT_DIR/bin/activate
python3 $CHECKOUT_DIR/metal_ping_disco_data_runner.py