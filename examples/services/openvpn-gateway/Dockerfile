FROM alpine:3.22

RUN apk add --no-cache \
    ca-certificates \
    iproute2 \
    iptables \
    openvpn \
    socat \
    tini

COPY entrypoint.sh /usr/local/bin/openvpn-gateway
RUN chmod 0755 /usr/local/bin/openvpn-gateway

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/openvpn-gateway"]
