from ripper.Ripper import Ripper
import getopt
import sys


def main(argv):
    banner()
    dictionary = None
    use_tor = False
    user = None
    users = None
    session = None

    try:
        opts, args = getopt.getopt(argv, "d:u:htf:s:", ["dictionary=", "user=", "help", "use-tor", "users-file=",
                                                        "session-file="])
    except getopt.GetoptError as err:
        print(err)
        usage()

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
            users = arg
        if opt in ("-s", "--session"):
            session = arg

    if users is None and user is None and session is None:
        usage()
    ripper = Ripper(target=user, targets=users, dictionary=dictionary, use_tor=use_tor, session=session)
    ripper.execute()


def usage():
    print("MoodleRipper v0.2:\n")
    print("usage: {} [arguments]\n".format(sys.argv[0]))
    print("Arguments:")
    print("  -h, --help                 Prints this message.")
    print("  -u, --user=<string>        Specify user's name to login.")
    print("  -f, --users_file=<file>    Load user names from text file.")
    print("  -d, --dictionary=<file>    Filename of desired dictionary, if it isn't specified default will be used.")
    print("  -t, --use-tor              Connect via Tor.")
    print("  -s, --session=<file>       Load session file.\n")
    print("Configuration:")
    print("Configuration options are in 'config.json' file. In this file you can change tor address, target address,")
    print("modify path of the login page and add or modify login parameters (default file has moodle defaults). ")
    quit()


def banner():
    art = "       __..._  _...__         ,__ __                        _         , __                                \n"
    art += "  _..-\"     `Y`      \"-._    /|  |  |                  |   | |       /|/  \  o                           \n"
    art += " \           |           /    |  |  |    __    __    __|   | |   _    |___/         _      _    _    ,_   \n"
    art += "  \\          |          //    |  |  |   /  \_ /  \_ /  |   |/   |/    | \    |    |/ \_  |/ \_ |/   /  |  \n"
    art += "  \\\         |         ///    |  |  |_/ \__/  \__/  \_/|_/ |__/ |__/  |  \_/ |_/  |__/   |__/  |__/    |_/\n"
    art += "   \\\ _..---.|.---.._ ///                                                        /|     /|                \n"
    art += "    \\`_..---.Y.---.._`//      by @iordic                                         \|     \|                \n"
    art += "     '`               `'                                                                                   \n"
    print(art)


if __name__ == "__main__":
    main(sys.argv[1:])
