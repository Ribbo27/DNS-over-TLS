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

### Questions

- Imagine this proxy being deployed in an infrastructure. What would be the security concerns you would raise?
  If the proxy is accessible from the external network, the proxy is subject to several types of attacks, like DDOS attacks, man in the middle, etc.
  If, on the other hand, it is only accessible from the local network, the biggest concern is the fact that the connection between the client and the proxy is not encrypted.

- How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?
  This proxy can be easily integrated in an architecture like the one mentioned in the question due to its design.
  There are different solutions to integrate it, the one I would use would be to set up load balancers in front of it to balance the load and allow to scale the service horizontally by adding more instances of it.

- What other improvements do you think would be interesting to add to the project?
  A simple but useful improvement would be to create a cache for the most frequent queries to speed up response times.

### References

- https://docs.python.org/3.8/library/socket.html#
- https://docs.python.org/3.8/library/ssl.html
- https://docs.docker.com/reference/