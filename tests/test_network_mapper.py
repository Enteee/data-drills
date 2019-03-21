# vim: set fenc=utf8 ts=4 sw=4 et :

import unittest
import ipaddress

from network_mapper import network_mapper

class TestNetworkMapper(unittest.TestCase):

    def test_subnet_mapping(self):
        nm = network_mapper.NetworkMapper([
            ipaddress.ip_network('0.0.0.0/24'),
            ipaddress.ip_network('1.0.0.0/24'),
            ipaddress.ip_network('2.0.0.0/24'),
        ])
        self.assertEqual(
            nm.map(ipaddress.ip_address('0.0.0.1')),
            ipaddress.ip_network('0.0.0.0/24')
        )
        self.assertNotEqual(
            nm.map(ipaddress.ip_address('0.0.1.1')),
            ipaddress.ip_network('0.0.0.0/24')
        )

    def test_most_specific_subnet(self):
        nm = network_mapper.NetworkMapper([
            ipaddress.ip_network('0.0.0.0/8'),
            ipaddress.ip_network('0.0.0.0/16'),
            ipaddress.ip_network('0.0.0.0/24'),
            ipaddress.ip_network('0.0.0.0/32'),
        ])
        self.assertEqual(
            nm.map(ipaddress.ip_address('0.0.0.0')),
            ipaddress.ip_network('0.0.0.0/32')
        )
        self.assertEqual(
            nm.map(ipaddress.ip_address('0.0.0.1')),
            ipaddress.ip_network('0.0.0.0/24')
        )

if __name__ == '__main__':
    unittest.main()
