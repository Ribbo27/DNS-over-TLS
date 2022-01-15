FROM ubuntu:latest

LABEL DOT container

WORKDIR /usr/bin/
COPY dot-proxy.py /usr/bin/dot-proxy.py

RUN chmod 755 /usr/bin/dot-proxy.py

EXPOSE 5300 53/tcp

CMD ["python3", "dot-proxy.py"]