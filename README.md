## metal_ping_disco

`metal_ping_disco` is a *"demo"* application intended to be used as a mock or stand-in for what a Metal Operator's application could be. It is strictly a lab or demo project, not to be associated with any kind of production setting. When provisioned it will provide a dashboard with a graph of the observed latency between the Equinix Metal host application is hosted on and various pre-defined pingable endpoints.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

![](https://s3.us-east-1.wasabisys.com/metalstaticassets/metal_ping_disco.JPG)

`metal_ping_disco` is really two little applications. 
* `metal_ping_disco.py` is meant to be a stateless but long-lived HTTP / browser reachable endpoint that loads data from S3, where that data would be collected by `metal_disco_data_runner.py`
* `metal_ping_disco_data_runner.py` is meant to be a scheduled taks (cronjob) that when executed, will load the previous runs dataset (if not found, create) and then ping a collection of endpoints, mangle the data into `.csv`, and then store that file back to S3. 

`data_runner` runs, collects, packages, exits & `ping_disco` runs and graphs and refreshes the browser from with newly collected data. By default every 10 seconds.

If this looks useful, you likely really want a real production ready tool such as:
* [smokeping](https://oss.oetiker.ch/smokeping/)
	* There is a Metal [specific smokeping document here](https://github.com/dlotterman/metal_code_snippets/tree/main/smokeping)
* [ping-statsd](https://github.com/chendo/ping-statsd)
* [ping_exporter for promethes](https://github.com/czerwonk/ping_exporter)

### Installation

As is, these applications are intended to be run as containerized applications, and should be deployed via `docker`, `podman` or `containerd`.

Both [metal_ping_disco] and [metal_ping_disco.py] are hosted on Dockerhub.

Environment Specific Steps:
- [docs/docker.md](Docker)
- [docs/podman.md](Podman)
- [docs/k8s.md](Kubernetes)
- *Coming soon - systemd*

### Credentials

The below environment variables need to be set:

```
export METAL_PING_DISCO_AWS_S3_BUCKET= \
export METAL_PING_DISCO_AWS_ACCESS_KEY_ID= \
export METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY= \
export METAL_PING_DISCO_AWS_S3_ENDPOINT=
```

These set the s3 endpoint (and provider), bucket name and credentials both applications will use. Note that the host does not need to be AWS S3 itself, just s3 protocol compliant. 