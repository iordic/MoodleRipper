import subprocess
import requests
import time
import os

TOR_CHECK_ADDRESS = 'https://check.torproject.org/api/ip'
TOR_APPLICATION = os.path.dirname(os.getcwd()) + '/tools/tor/Tor/tor.exe'
TOR_STRING_SUCCESS = "100% (done): Done"    # Check at stdout if tor has executed successfully
MAX_WAIT_TIME = 60  # Seconds to wait for tor execution


class SocketLayer:
    user_agent = None
    config = None
    python_child = None

    def __init__(self, configuration):
        self.config = configuration
        self.session = requests.session()
        self.session.headers.update({'User-Agent': self.config.selected_agent})
        if self.config.use_tor:
            self.session.proxies = {'http': self.config.proxy, 'https': self.config.proxy}
            if not self.check_tor():
                if os.name == 'nt':
                    print("Windows detected: Trying to run a tor process... ", end="")
                    self.create_tor_process()
                    if self.python_child is None:
                        print("FAILURE")
                        print("Exiting...")
                        quit()
                    else:
                        print("SUCCESS")
                else:
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

    def create_tor_process(self):
        self.python_child = subprocess.Popen(TOR_APPLICATION, stdout=subprocess.PIPE)
        initial_time = time.time()
        while TOR_STRING_SUCCESS.encode() not in self.python_child.stdout.readline():
            time.sleep(1)
            current_time = time.time()
            if current_time - initial_time > MAX_WAIT_TIME:
                print("Exceeded time, aborting...")
                self.python_child.kill()
                self.python_child = None

    def get_json(self, address):
        response = self.session.get(address)
        return response.json()

    def close_session(self):
        if self.python_child is not None:
            self.python_child.kill()
        self.session.close()
