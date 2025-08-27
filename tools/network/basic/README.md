# Testing Device to Device Bandwidth with iPerf3

On the server, where bandwidths are tested to and from, run this command:

```bash
iperf3 -s
```

When installed on the server, iPerf3 can actually be launched as a daemon so a test can always be run against it. Neat!

On the remote device, where the test originates from, run this command:

```bash
iperf3 -c <Server IP>
```

This requires the default iPerf3 port of 5201 to be opened through the firewall.

```bash
sudo ufw allow 5201
```
