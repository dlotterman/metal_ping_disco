# -*- coding: utf-8 -*-
import datetime
import subprocess
import logging
import os
import sys
import time

import pandas as pd

import mysql.connector as mysqldb

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"
)

AWS_S3_BUCKET = os.getenv("METAL_PING_DISCO_AWS_S3_BUCKET")
AWS_ACCESS_KEY_ID = os.getenv("METAL_PING_DISCO_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT = os.getenv("METAL_PING_DISCO_AWS_S3_ENDPOINT")
MYSQL_ENDPOINTS_RAW = os.getenv("METAL_PING_DISCO_MYSQL_ENDPOINTS_RAW")

MYSQL_ENDPOINTS = [
]

endpoints = [
    "metal_dc13:136.144.56.179",
    "metal_hk2:145.40.125.17",
    "metal_sk2:147.28.173.3",
    "metal_ch3:145.40.75.3",
    "metal_am6:147.75.87.3",
    "aws_us_west1:13.56.63.251",
    "aws_us_east1:3.208.0.0",
    "aws_us_central1:3.120.0.0",
    "opendns:208.67.222.222",
]

def process_mysql_endpoints():

    for ENDPOINT in MYSQL_ENDPOINTS_RAW.split(','):
        MYSQL_ENDPOINTS.append(ENDPOINT)

def metal_ping_disco():
    logging.info("starting metal_ping_disco data collection")
    process_mysql_endpoints()

    try:
        network_data = pd.read_csv(
            "s3://{}/metal_ping_disco_network_data.csv".format(AWS_S3_BUCKET),
            storage_options={
                "key": AWS_ACCESS_KEY_ID,
                "secret": AWS_SECRET_ACCESS_KEY,
                "client_kwargs": {
                    "endpoint_url": AWS_S3_ENDPOINT,
                },
            },
        )
    except FileNotFoundError:
        logging.warning(
            "metal_ping_disco_network_data.csv not found in s3 bucket, will attempt to seed a new data file"
        )
        network_data = pd.DataFrame(columns=["ip", "time", "latency"])

    except:
        logging.exception("Fatal error interacting with s3, exiting")
        sys.exit(1)

    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for endpoint in endpoints:
        ping_output = subprocess.run(
            ["ping", endpoint.split(":")[1], "-c", "1", "-w", "2"],
            timeout=10,
            capture_output=True,
        )
        endpoint_latency = str(ping_output.stdout).split("/")[3].split("=")[1].lstrip()
        network_data_collected = pd.DataFrame(
            [[endpoint, ts, endpoint_latency]], columns=["ip", "time", "latency"]
        )
        network_data = pd.concat(
            [network_data, network_data_collected], ignore_index=True
        )
    for mysql_endpoint in MYSQL_ENDPOINTS:
        name = mysql_endpoint.split(':')[0]
        host = mysql_endpoint.split(':')[1]
        port = mysql_endpoint.split(':')[2]
        username = mysql_endpoint.split(':')[3]
        password = mysql_endpoint.split(':')[4]
        database = mysql_endpoint.split(':')[5]
        tic = time.time()
        try:
            connection = mysqldb.connect(
                user=username,
                password=password,
                host=host,
                database=database)
            if connection.is_connected():
                dbinfo = connection.get_server_info()
                toc = time.perf_counter()
                connection.close()
                latency = time.time() - tic
        except Error as e:
            logging.error('Error connecting to %s mysql endpoint', mysql_endpoint)
        finally:
            logging.info('%s latency time is %.4f', mysql_endpoint, latency)
            network_data_collected = pd.DataFrame(
                [[name, ts, endpoint_latency]], columns=["ip", "time", "latency"]
            )
            network_data = pd.concat(
                [network_data, network_data_collected], ignore_index=True
            )          

    network_data.to_csv(
        "s3://{}/metal_ping_disco_network_data.csv".format(AWS_S3_BUCKET),
        index=False,
        storage_options={
            "key": AWS_ACCESS_KEY_ID,
            "secret": AWS_SECRET_ACCESS_KEY,
            "client_kwargs": {
                "endpoint_url": AWS_S3_ENDPOINT,
            },
        },
    )


if __name__ == "__main__":
    metal_ping_disco()


### Docs:

# The python line endpoint_latency = str(ping_output.stdout).split('/')[3].split('=')[1].lstrip()
# Takes the below output from a shell ping command:
# b'PING 136.144.56.179 (136.144.56.179) 56(84) bytes of data.\n64 bytes from 136.144.56.179: icmp_seq=1 ttl=63 time=71.7
# ms\n\n--- 136.144.56.179 ping statistics ---\n1 packets transmitted, 1 received, 0% packet loss, time 0ms\nrtt min/avg/m
# ax/mdev = 71.708/71.708/71.708/0.000 ms\n'

# and isolates it to the string:
# 73.088

# The reason why we use subprocess / shell's ping is that most distro's implement a setuid on the ping binary that allows
# non-root users to execute it. Otherwise tooling in python that creates ICMP traffic needs root privs to do so because
# python does not replicate that setuid behavior and replicating it would be burdensome. Running a container as root is bad
# so we do a slightly less bad thing and shell out from python so we can do the needful with minimal privs
