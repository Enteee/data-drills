# vim: set fenc=utf8 ts=4 sw=4 et :
import logging
import ipaddress
import typing

class NetworkMapper(object):
    """Maps ip addresses to best matching subnet."""

    def __init__(self, networks: typing.Iterable[ipaddress.ip_network]) -> None:
        self.__logger = logging.getLogger(__name__)
        self.__networks = networks

    def map(self, ip: ipaddress.ip_address) -> ipaddress.ip_network:
        most_specific_subnet = ipaddress.ip_network('0.0.0.0/0')
        for network in self.__networks:
            if ip in network \
                and network.subnet_of(most_specific_subnet):
                    most_specific_subnet = network
        return most_specific_subnet
