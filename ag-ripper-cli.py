from ripper.Ripper import Ripper
import getopt
import json
import sys


def main(argv):
    banner()
    dictionary = None
    use_tor = False
    user = None
    users = None
    try:
        opts, args = getopt.getopt(argv, "d:u:htf:", ["dictionary=", "user=", "help", "use-tor", "users-file="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        quit()
    for opt, arg in opts:
        if opt in ('-h', "--help"):
            usage()
            quit()
        if opt in ('-d', "--dictionary"):
            dictionary = arg
        if opt in ("-t", "--use-tor"):
            use_tor = True
        if opt in ("-u", "--user"):
            user = arg
        if opt in ("-f", "--users-file"):
            with open(arg, 'r') as users_file:
                users = json.load(users_file)
    if user is not None and users is None:
        ripper = Ripper(dictionary, use_tor)
        result = ripper.execute(user)
        print("Result:")
        print(result)
    elif user is None and users is not None:
        ripper = Ripper(dictionary, use_tor)
        print("Results:")
        for user in users:
            result = ripper.execute(user)
            print(result)
    else:
        print("ERROR: You must specify an user")
        usage()


def usage():
    print("Moodle Ripper v0.1 by @iordic:\n")
    print("usage: ag-ripper-cli.py [arguments]\n")
    print("Arguments:")
    print("-h, --help                 Prints this message.")
    print("-u, --user=<string>        Specify user's name to login.")
    print("-f, --users_file=<file>    Charge uses from text file (in JSON format).")
    print("-d, --dictionary=<file>    Filename of desired dictionary, if it isn't specified default will be used.")
    print("-t, --use-tor              Connect via Tor.\n")
    print("Configuration:")
    print("Configuration options are in 'config.json' file. In this file you can change tor address, target address,")
    print("modify path of the login page and add or modify login parameters (default file has moodle defaults). ")


def banner():
    print()


if __name__ == "__main__":
    main(sys.argv[1:])
