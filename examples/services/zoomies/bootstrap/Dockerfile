FROM alpine:3.22

RUN apk add --no-cache findutils util-linux

COPY bootstrap/entrypoint.sh /usr/local/bin/zoomies-host-bootstrap
COPY bootstrap-host.sh /opt/zoomies/host-bootstrap.sh
RUN chmod 0755 /usr/local/bin/zoomies-host-bootstrap /opt/zoomies/host-bootstrap.sh

ENTRYPOINT ["/usr/local/bin/zoomies-host-bootstrap"]
