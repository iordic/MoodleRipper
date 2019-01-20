import unittest
from ripper.SocketLayer import SocketLayer
import json


class TestSocketLayer(unittest.TestCase):

    def setUp(self):
        self.socket = SocketLayer(False)        # plain connection
        self.tor_socket = SocketLayer(True)     # tor connection

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
        with open('../resources/user_agents.json', 'r') as ags:
            agents = json.load(ags)
        response = self.socket.get_json('https://httpbin.org/headers')
        response_agent = response['headers']['User-Agent']
        self.assertTrue(response_agent in agents)
