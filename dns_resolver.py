"""Monitor docker containers and add their dns hostnames."""
import sys
from os import environ
from time import sleep

import docker
from logzero import logger
from python_hosts import Hosts, HostsEntry

DNS_REFRESH_TIME_S = float(environ.get('DNS_REFRESH_TIME_S'))
DNS_FILTER_CONTAINS = environ.get('DNS_FILTER_CONTAINS')
HOST_PATH = environ.get('HOST_PATH')

CLIENT = docker.from_env()
HOSTS = Hosts(path=HOST_PATH)

ENTRIES = {}

if __name__ == '__main__':
    while True:
        for container in CLIENT.containers.list():
            networks = container.attrs['NetworkSettings']['Networks']
            conf = container.attrs['Config']

            if not (conf['Hostname'] and conf['Domainname']):
                continue
            hostname = '{}.{}'.format(conf['Hostname'], conf['Domainname'])

            for nw_name in networks:
                network = networks[nw_name]
                ip = network['IPAddress']

                if DNS_FILTER_CONTAINS in hostname:
                    if container.status == 'running':
                        if hostname not in ENTRIES:
                            ENTRIES[hostname] = HostsEntry(
                                entry_type='ipv4',
                                address=ip,
                                names=[hostname])
                            logger.info('add %s to HOSTS', hostname)
                            HOSTS.add([ENTRIES[hostname]])
                    else:
                        if hostname in ENTRIES:
                            del ENTRIES[hostname]
                            HOSTS.remove_all_matching(name=hostname)
                            logger.info('remove %s from HOSTS', hostname)

        HOSTS.write()
        sleep(DNS_REFRESH_TIME_S)
