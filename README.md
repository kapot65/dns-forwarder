# Docker dns forwarder

Simple docker service that resolves internal docker-compose containers
hostnames to host /etc/hosts file.

## Usage
Service example in docker-compose file:
```yaml
dns:
  restart: unless-stopped
  build: ${PWD}/dns-forwarder
  networks:
    - docker_network
  hostname: ${DNS_SERVER_HOSTNAME}
  volumes:
     - /etc/hosts:/usr/src/hosts
     - /var/run/docker.sock:/var/run/docker.sock
  tty: true
  environment:
    DNS_REFRESH_TIME_S: 5 # dns updates check rate in s (default: 5)
    DNS_FILTER_CONTAINS: intranet  # containers hostname
                                   # contains filter
                                   # (default: intranet)
    HOST_PATH: /usr/src/hosts # internal hosts file path
                              # (default: /usr/src/hosts)
```

> **Warning:**
> Service should stops gracefully, otherwise it won't flush /etc/host
> back to original values.
