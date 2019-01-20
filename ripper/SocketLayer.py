import requests
import random
import json


class SocketLayer:
    user_agent = None
    config = None
    # Files
    AGENTS_FILE = "resources/user_agents.json"
    CONFIG_FILE = "resources/config.json"

    def __init__(self, use_tor=False, user_agent=None):
        self.session = requests.session()
        if user_agent is None:
            # If user agent is not define, choice a random one from user agents file
            with open(self.AGENTS_FILE) as agents:
                agents_array = json.load(agents)
                selected_agent = random.choice(agents_array)    # Select random agent from file
            self.session.headers.update({'User-Agent': selected_agent})
        else:
            self.session.headers.update({'User-Agent': user_agent})
        with open(self.CONFIG_FILE) as conf:
            self.config = json.load(conf)
        if use_tor:
            self.session.proxies = {'http': self.config['tor_address'], 'https': self.config['tor_address']}

    def try_login(self, user, password):
        url = self.config['url'] + self.config['path']
        self.config['parameters']['username'] = user
        self.config['parameters']['password'] = password
        response = self.session.get(url, params=self.config['parameters'])
        return response.json()

    def check_tor(self):
        response = self.session.get('https://check.torproject.org/api/ip')
        return response.json()['IsTor']

    def get_json(self, address):
        response = self.session.get(address)
        return response.json()

    def close_session(self):
        self.session.close()
