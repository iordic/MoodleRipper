from resources.Configuration import Configuration
from ripper.SocketLayer import SocketLayer
import unittest


class TestSocketLayer(unittest.TestCase):

    def setUp(self):
        self.tor_configuration = Configuration(use_tor=True)
        self.plain_configuration = Configuration()
        self.socket = SocketLayer(self.plain_configuration)     # plain connection
        self.tor_socket = SocketLayer(self.tor_configuration)   # tor connection

    def tearDown(self):
        self.socket.close_session()             # close both sockets
        self.tor_socket.close_session()

    def test_tor_connection(self):
        response = self.tor_socket.check_tor()
        self.tor_socket.close_session()
        self.assertTrue(response)

    def test_tor_connection2(self):
        tor_response = self.tor_socket.get_json("https://httpbin.org/ip")
        self.tor_socket.close_session()
        plain_response = self.socket.get_json("https://httpbin.org/ip")
        self.assertFalse(plain_response['origin'] == tor_response['origin'])

    def test_plain_connection(self):
        response = self.socket.check_tor()
        self.assertFalse(response)

    def test_user_agent(self):
        response = self.socket.get_json('https://httpbin.org/headers')
        response_agent = response['headers']['User-Agent']
        self.assertTrue(response_agent in self.plain_configuration.selected_agent)
