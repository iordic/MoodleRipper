import requests

TOR_CHECK_ADDRESS = 'https://check.torproject.org/api/ip'


class SocketLayer:
    user_agent = None
    config = None

    def __init__(self, configuration):
        self.config = configuration
        self.session = requests.session()
        self.session.headers.update({'User-Agent': self.config.selected_agent})
        if self.config.use_tor:
            self.session.proxies = {'http': self.config.proxy, 'https': self.config.proxy}
            if not self.check_tor():
                print("Tor proxy is not running, aborting.")
                quit()

    def try_login(self, user, password):
        url = self.config.url_target
        self.config.parameters['username'] = user
        self.config.parameters['password'] = password
        response = self.session.get(url, params=self.config.parameters)
        return response.json()

    def check_tor(self):
        try:
            response = self.session.get(TOR_CHECK_ADDRESS)
            return response.json()['IsTor']
        except requests.RequestException:
            return False

    def get_json(self, address):
        response = self.session.get(address)
        return response.json()

    def close_session(self):
        self.session.close()
