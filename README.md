# N26 - SRE Challenge

## Requirements

From your understanding of the topic, we would expect a working example of a DNS to
DNS-over-TLS proxy that can:
1. Handle at least one DNS query, and give a result to the client.
2. Work over TCP and talk to a DNS-over-TLS server that works over TCP (e.g: Cloudflare).

## Quickstart

Execute the build script:

`./build.sh`

At this point you should have a TCP server listening on port 5300.

### How to access the container

To access the container, just run:

`sudo docker exec -it dot-proxy-container /bin/bash`

### Test 

Get the IP of your running container(usually `172.17.0.2` on **linux** machines):

`sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dot-proxy-container`

Then test the DNS proxy with the `dig` cmd:

`dig n26.com +tcp -d @172.17.0.2 -p 5300 -t A`


### References

- https://docs.python.org/3.8/library/socket.html#
- https://docs.python.org/3.8/library/ssl.html
- https://docs.docker.com/reference/