# N26 - SRE Challenge

## Requirements

From your understanding of the topic, we would expect a working example of a DNS to
DNS-over-TLS proxy that can:
1. Handle at least one DNS query, and give a result to the client.
2. Work over TCP and talk to a DNS-over-TLS server that works over TCP (e.g: Cloudflare).

## Solution explanation

This simple proxy is set by default to send DNS queries to Cloudflare.

The script will create a TCP listener on port `5300`.
Whenever a request is sent to the server, a new process will be created which will invoke the `tcp_handler` function.
The `tcp_handler` function is responsible for forwarding the request to the `dns_query` function.
The `dns_query` function is in charge of establishing a TLS connection with the DNS service, in this case Cloudflare, and after that sending the DNS query to it.
Once the DNS server has responded, the `tcp_handler` function will send the response back to the client.

NOTE: The server only support TCP request, UDP was not implemented. In addition, it can handle multiple requests at the same time.


## Quickstart

Execute the build script:

`./build.sh`

At this point you should have a TCP server listening on port 5300.

### How to test 

Get the IP of your running container(usually `172.17.0.2` on **linux** machines):

`sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dot-proxy-container`

Then test the DNS proxy with the `dig` cmd (of course you can also use `kdig`, `nslookup`, `wireshark` or whatever tool you prefer :) ):

`dig n26.com +tcp -d @172.17.0.2 -t A`

Multiple incoming requests handling was also tested, some results:

![Testing multiple incoming requests](https://user-images.githubusercontent.com/35638854/149642575-a74d885b-c1b9-4964-b686-dad3b2158b28.png)

### How to access the container

To access the container, just run:

`sudo docker exec -it dot-proxy-container /bin/bash`

### Questions

- Imagine this proxy being deployed in an infrastructure. What would be the security concerns you would raise?
  Suppose that the proxy is accessible only from the local network, someone who has access to it could leverage the fact that client-proxy connection is not encrypted. This expose the service to a man in the middle attack.

  If the proxy is accessible from the external network, the proxy is subject to several types of attacks, like DDOS attacks, man in the middle, etc.
  If, on the other hand, it is only accessible from the local network, the biggest concern is the fact that the connection between the client and the proxy is not encrypted.

- How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?
  This proxy can be integrated in an architecture like the one mentioned in the question due to its design.
  There are different solutions to integrate it, the one I would use would be to scale it horizontally first, so deploy multiple instances in different availability domains to ensure HA and set up load balancers in front of it to balance the load and to add another layer that can be used for example to enhance the security. Then if an higer throughput is need it can also be scaled vertically adding more power to the machines.

- What other improvements do you think would be interesting to add to the project?
  Some features that can be added could be:
    - Cache: Implement a cache system to store most frquent queries in order to speed up response times.
    - DoH: Another nice to have feature would be to support also DNS over HTTPS.
    - Implement some sort of protection against DOS attacks, blocking IPs that try to send a large number of requests in a reasonable timeframe.

### References

- https://docs.python.org/3.8/library/socket.html#
- https://docs.python.org/3.8/library/ssl.html
- https://docs.docker.com/reference/