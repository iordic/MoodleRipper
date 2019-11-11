from os.path import dirname
import random
import json


# Constants
DIRNAME = dirname(__file__)     # Get absolute path of current file
USER_AGENTS_FILE = DIRNAME + '/user_agents.txt'
DICTIONARY_FILE = DIRNAME + '/dictionary.txt'
CONFIG_FILE = DIRNAME + '/config.json'


class Configuration:
    def __init__(self, targets=None, use_tor=False, dictionary=DICTIONARY_FILE):
        # Load configuation values
        config = json_parse(CONFIG_FILE)
        # Configuration file values
        self.url_target = config['url'] + config['path']
        self.parameters = config['parameters']
        self.proxy = config['proxy']    # Tor proxy
        # Value tuples
        self.user_agents = tuple(text_to_list(USER_AGENTS_FILE))
        self.dictionary = tuple(text_to_list(dictionary))
        # Other configuration
        self.use_tor = use_tor
        self.targets = targets  # Users to attack
        self.selected_agent = random.choice(self.user_agents)   # Choice random agent
        self.checked_targets = []

    def __str__(self):
        result = "Current configuration:\n"
        result += "=====================\n"
        result += "  + Target url: {}\n".format(self.url_target)
        result += "  + Users: {}\n".format(self.targets)
        if self.use_tor:
            result += "  + Using tor proxy: {}\n".format(self.proxy)
        result += "  + User agent: {}\n".format(self.selected_agent)
        return result

    def change_user_agent(self):
        self.selected_agent = random.choice(self.user_agents)

    def next_target(self, result):
        self.checked_targets.append(result)


# Aux functions
def text_to_list(file_path):
    aux_list = []
    f = open(file_path, 'r')
    for line in f:
        aux = line.strip()
        if aux == '':
            continue
        aux_list.append(aux)
    f.close()
    return aux_list


def json_parse(file_path):
    f = open(file_path, 'r')
    parsed = json.load(f)
    f.close()
    return parsed
