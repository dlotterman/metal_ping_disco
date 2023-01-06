## metal_ping_disco

THIS IS STILL BROKEN

* Write the systemd unit file out:

```
[Unit]
Description=metal_ping_disco
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
Environment="CHECKOUT_DIR/bin"
ExecStart="CHECKOUT_DIR/bin/python3 $CHECKOUT_DIR/metal_ping_disco.py"

[Install]
WantedBy=multi-user.target
```

* Reload systemd unit file config
	- `sudo systemctl daemon-reload`

## metal_ping_disco_data_runner

* Copy the `metal_ping_disco_data_runner_wrapper.sh` script somewhere (I like `/dev/shm/` because if I store secrets in that file they are in memory and lost on reboot):

	- `cp metal_ping_disco_data_runner_wrapper.sh /dev/shm/`

* Edit the file to update the appropriate exports.

* Add the crontab line:
	- `echo "*/5 *   * * *   root bash /dev/shm/metal_ping_disco_data_runner_wrapper.sh" | sudo tee -a /etc/crontab`
