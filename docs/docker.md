It is expected that the container toolchain of choice (docker, podman etc) is already installed and correctly configured for container deployments.

* [Docker Install Documentation](https://docs.docker.com/engine/install/ubuntu/)

## metal_ping_disco

To pull the image from Docker Hub to the local registry:

`sudo docker pull dlotterman/metal_ping_disco:latest`

Start the docker container:

```
sudo docker run -d --name metal_ping_disco_1 \
-e METAL_PING_DISCO_AWS_S3_BUCKET=$METAL_PING_DISCO_AWS_S3_BUCKET \
-e METAL_PING_DISCO_AWS_ACCESS_KEY_ID=$METAL_PING_DISCO_AWS_ACCESS_KEY_ID \
-e METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY=$METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY \
-e METAL_PING_DISCO_AWS_S3_ENDPOINT=$METAL_PING_DISCO_AWS_S3_ENDPOINT \
-p 8050:8050/tcp dlotterman/metal_ping_disco
```

Where the [environment variables have already be exported per the repo README](../README.md)

Confirm the Container is running:

```
$ sudo docker ps
CONTAINER ID   IMAGE                         COMMAND                  CREATED          STATUS          PORTS                                       NAMES
b47cf678ef2f   dlotterman/metal_ping_disco   "python metal_ping_d…"   54 minutes ago   Up 54 minutes   0.0.0.0:8050->8050/tcp, :::8050->8050/tcp   metal_ping_disco
```

The dashboard should be available by browser at `http://YOUR_IP:8050`

## metal_ping_disco_data_runner

To pull the image from Docker Hub to the local registry:

`sudo docker pull dlotterman/metal_ping_disco_data_runner:latest`

Start the docker container:

```
sudo docker run -d --name metal_ping_disco_data_runner \
-e METAL_PING_DISCO_AWS_S3_BUCKET=$METAL_PING_DISCO_AWS_S3_BUCKET \
-e METAL_PING_DISCO_AWS_ACCESS_KEY_ID=$METAL_PING_DISCO_AWS_ACCESS_KEY_ID \
-e METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY=$METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY \
-e METAL_PING_DISCO_AWS_S3_ENDPOINT=$METAL_PING_DISCO_AWS_S3_ENDPOINT \
dlotterman/metal_ping_disco_data_runner
```

Once the container has been instantiated with the environment variables, it can be re-run as needed with just 

`sudo docker restart metal_ping_disco_data_runner`.

It can be added to cron to run every 5 minutes:

`echo "*/5 *   * * *   root docker restart metal_ping_disco_data_runner" | sudo tee -a /etc/crontab`