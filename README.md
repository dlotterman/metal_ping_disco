## metal_ping_disco

`metal_ping_disco` is a *"demo application"*  intended to be used as a mock or stand-in for what a Metal Operator's application could be. It is strictly a lab or demo project, not to be associated with any kind of production setting. When provisioned it will provide a dashboard with a graph of the observed latency between the Equinix Metal host application is hosted on and various pre-defined pingable endpoints.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

![](https://s3.us-east-1.wasabisys.com/metalstaticassets/metal_ping_disco.JPG)

`metal_ping_disco` is really two little applications:
* `metal_ping_disco.py` is meant to be a stateless but long-lived HTTP / browser reachable endpoint that loads data from s3 (collected by `data_runner`), and graphs it.
* `metal_ping_disco_data_runner.py` is meant to be a scheduled taks (cronjob) that when run, will load the previous runs dataset (if not found, create) and then ping a collection of endpoints, mangle the data into `.csv`, and then store that file back to s3. 

If this looks useful, you likely really want a real production ready tool such as:
* [smokeping](https://oss.oetiker.ch/smokeping/)
	* There is a Metal [specific smokeping document here](https://github.com/dlotterman/metal_code_snippets/tree/main/smokeping)
* [ping-statsd](https://github.com/chendo/ping-statsd)
* [ping_exporter for prometheus](https://github.com/czerwonk/ping_exporter)

### Installation

These applications are intended to be run as containerized applications, and should be deployed via `docker`, `podman` or `containerd`.

Both [metal_ping_disco](https://hub.docker.com/repository/docker/dlotterman/metal_ping_disco) and [metal_ping_disco_data_runner](https://hub.docker.com/repository/docker/dlotterman/metal_ping_disco_data_runner) are hosted on Dockerhub.

Environment Specific Steps:
- [Docker](docs/docker.md)
- [Podman](docs/podman.md)
- [Kubernetes](docs/k8s.md)
- *Coming soon - systemd*

### Credentials

The below environment variables need to be set:

```
export METAL_PING_DISCO_AWS_S3_BUCKET= \
export METAL_PING_DISCO_AWS_ACCESS_KEY_ID= \
export METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY= \
export METAL_PING_DISCO_AWS_S3_ENDPOINT=
```

These set the s3 endpoint (and provider), bucket name and credentials both applications will use. Note that the s3 provider does not need to be AWS s3 itself, just s3 protocol compliant. 

#### Ping Monitoring
By default, Ping Disco will default to a handful of ICMP reachable endpoints. To specify your own, set the following environment variable:
```
export METAL_PING_DISCO_PING_ENDPOINTS_RAW="metal_sv15:136.144.55.31,metal_fr2:145.40.93.77,metal_dfw2:139.178.82.17" && \
```

Where
	- `metal_sv15` will be the name of the graph legend for the edpoint, and `136.144.55.31` is the IP address of the endpoint to ping. DNS names *should* work fine.

#### MySQL Monitoring
Optionally, set:
```
export METAL_PING_DISCO_MYSQL_ENDPOINTS_RAW="haha_db:127.0.0.1:3306:disco_user:disco_Pass:disco_db,haha_db2:127.0.0.2:3306:disco_user:disco_Pass:disco_db"
```

This will enable tell the container to make a MySQL query and measure the latency for:
	- `127.0.0.1` on port `3306` with the user `disco_user` with the password `disco_Pass`, where the line on the graph and legend will be `haha_db`, and then all the same for `haha_db2` on IP `127.0.0.2`.
	- Values for each mysql instance are colon seperated, mysql instances themselves are comma seperated.
	
#### Oracle Monitoring:
Optionally, set:
```
export METAL_PING_DISCO_ORACLE_ENDPOINTS_RAW="oracle_db:139.178.94.137/xe:1521:oracle_user:oracle_pass,"
```

This will enable tell the container to make a OracleDB query and measure the latency for:
	- `139.178.94.137` on port `1521` with the user `oracle_user` with the password `oracle_pass`, where the line on the graph and legend will be `oracle_db`
	- Values for each oracle instance are colon seperated, oracle instances themselves are comma seperated.