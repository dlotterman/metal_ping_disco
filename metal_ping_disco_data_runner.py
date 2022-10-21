# -*- coding: utf-8 -*-
import datetime
import subprocess
import logging
import os
import sys

import pandas as pd


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

AWS_S3_BUCKET = os.getenv("METAL_PING_DISCO_AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("METAL_PING_DISCO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT = os.getenv("METAL_PING_DISCO_AWS_S3_ENDPOINT")

endpoints = ['metal_dc13:136.144.56.179', 'metal_hk2:145.40.125.17', 'metal_sk2:147.28.173.3',
    'metal_ch3:145.40.75.3', 'metal_am6:147.75.87.3', 'aws_us_west1:13.56.63.251',
    'aws_us_east1:3.208.0.0', 'aws_us_central1:3.120.0.0', 'opendns:208.67.222.222']

def metal_ping_disco():

    logging.info('starting metal_ping_disco data collection')

    try:
        network_data = pd.read_csv(
            "s3://{}/metal_ping_disco_network_data.csv".format(AWS_S3_BUCKET),
            storage_options = {
                "key": AWS_ACCESS_KEY_ID,
                "secret": AWS_SECRET_ACCESS_KEY,
                "client_kwargs": {
                    "endpoint_url": AWS_S3_ENDPOINT,
                },
            },
        )
    except FileNotFoundError:
        logging.warning(
            'metal_ping_disco_network_data.csv not found in s3 bucket, will attempt to seed a new data file')
        network_data = pd.DataFrame(columns=['ip', 'time', 'latency'])

    except:
        logging.exception("Fatal error interacting with s3, exiting")
        sys.exit(1)

    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for endpoint in endpoints:
        ping_output = subprocess.run(['ping', endpoint.split(':')[1], '-c', '1', '-w', '2'], timeout=10, capture_output=True)
        endpoint_latency = str(ping_output.stdout).split('/')[3].split('=')[1].lstrip()
        network_data_collected = pd.DataFrame([[endpoint, ts, endpoint_latency]], columns=['ip', 'time', 'latency'])
        network_data = pd.concat([network_data, network_data_collected], ignore_index=True)

    network_data.to_csv(
        "s3://{}/metal_ping_disco_network_data.csv".format(AWS_S3_BUCKET),
        index=False,
            storage_options = {
                "key": AWS_ACCESS_KEY_ID,
                "secret": AWS_SECRET_ACCESS_KEY,
                "client_kwargs": {
                    "endpoint_url": AWS_S3_ENDPOINT,
                },
            },
        )

if __name__ == "__main__":
    metal_ping_disco()
