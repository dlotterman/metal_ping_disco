It is expected that the container toolchain of choice (docker, podman etc) is already installed and correctly configured for container deployments.

* [Podman Install Documentation](https://podman.io/getting-started/installation)

## metal_ping_disco

Pull the container from Docker Hub:

```
sudo podman pull dlotterman/metal_ping_disco:latest
✔ docker.io/dlotterman/metal_ping_disco:latest
Trying to pull docker.io/dlotterman/metal_ping_disco:latest...
Getting image source signatures
Copying blob d968c23ee1bf done  
Copying blob 2f7e702ad81b done  
Copying blob f413d878c196 done  
Copying blob eaa89787764f done  
Copying blob 4500a762c546 done  
Copying blob 3cf767885ed2 done  
Copying blob 11de582d7401 done  
Copying blob 761a0db30286 done  
Copying blob f58824b51a95 done  
Copying blob d4a15791e701 done  
Copying config 200ddba8a0 done  
Writing manifest to image destination
Storing signatures
200ddba8a0e1e2d5aaf89b89ad7d4ceea66e95548362db15f67143b3146fa185
```

Run the container:

```
sudo podman run -d --name metal_ping_disco \
-e METAL_PING_DISCO_AWS_S3_BUCKET=$METAL_PING_DISCO_AWS_S3_BUCKET \
-e METAL_PING_DISCO_AWS_ACCESS_KEY_ID=$METAL_PING_DISCO_AWS_ACCESS_KEY_ID \
-e METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY=$METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY \
-e METAL_PING_DISCO_AWS_S3_ENDPOINT=$METAL_PING_DISCO_AWS_S3_ENDPOINT \
-p 8050:8050/tcp dlotterman/metal_ping_disco
```

Where the [environment variables have already be exported per the repo README](../README.md)

The dashboard should be available by browser at `http://YOUR_IP:8050`

## metal_ping_disco_data_runner

To pull the image from Docker Hub to the local registry:

```
$ sudo podman pull dlotterman/metal_ping_disco_data_runner:latest
? Please select an image: 
    registry.access.redhat.com/dlotterman/metal_ping_disco_data_runner:latest
    registry.redhat.io/dlotterman/metal_ping_disco_data_runner:latest
  ▸ docker.io/dlotterman/metal_ping_disco_data_runner:latest
```

Start the docker container:

```
sudo podman run -d --name metal_ping_disco_data_runner \
-e METAL_PING_DISCO_AWS_S3_BUCKET=$METAL_PING_DISCO_AWS_S3_BUCKET \
-e METAL_PING_DISCO_AWS_ACCESS_KEY_ID=$METAL_PING_DISCO_AWS_ACCESS_KEY_ID \
-e METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY=$METAL_PING_DISCO_AWS_SECRET_ACCESS_KEY \
-e METAL_PING_DISCO_AWS_S3_ENDPOINT=$METAL_PING_DISCO_AWS_S3_ENDPOINT \
dlotterman/metal_ping_disco_data_runner
```
Once the container has been instantiated with the environment variables, it can be re-run as needed with just 

`sudo podman restart metal_ping_disco_data_runner`.

It can be added to cron to run every 5 minutes:

`echo "*/5 *   * * *   root podman restart metal_ping_disco_data_runner" | sudo tee -a /etc/crontab`