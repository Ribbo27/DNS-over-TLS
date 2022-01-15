#!/bin/bash

docker build -t dot-proxy .
docker run -d --net=bridge -p 5300:53 --name dot-proxy-container dot-proxy