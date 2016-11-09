#! usr/bin/env/python2
# main.py - driver for the lending system

import getopt

from loanOfficer import *


def main(argv):
    if len(sys.argv) <= 1:
        print """usage: main.py [command] [option(s)]
                commands        options
                --admin -a      N/A               login to the system as an adiministrator
                --customer -c   N/A"""
    try:
        opts, args = getopt.getopt(argv, "ca", ["admin", "customer"])
    except getopt.GetoptError:
        print """usage: main.py [command] [option(s)]
        commands        options
        --admin -a      [loan officer's user name]                login to the system as an adiministrator
        --customer -c   N/A                                       login as a customer """
    for opt, arg in opts:
        if opt.lower() in ("--admin", "-a"):
            officer = loanOfficer()
            choice = raw_input("What do you want to do? press CTRL+D to exit\n"
                               "1. Score customer\n"
                               "2. View customers details\n"
                               "3. Create a new admin\n"
                               "4. Logout\n"
                               "Continue with 1, 2, 3, 4: ")
            if choice == "1":
                officer.score_Customer()
                logout()
            elif choice == "2":
                officer.list_unscored_customers()
                logout()
            elif choice == "3":
                try:
                    officer.create_admin()
                    logout()
                except:
                    after_request_handler()
                    return "User with a similar username exists!"
            else:
                return logout()
        elif opt.lower() in ("-c"):
            choice = raw_input("What do you want to do? Press CTRL+D to exit\n"
                               "1. Request loan\n"
                               "2. Create an account\n"
                               "3. Quit\n"
                               "Continue with 1, 2 or 3: "
                               )
            if choice == "1":
                request_loan()
                logout()
            elif choice == "2":
                Create_usr()
                logout()
            else:
                logout()
            after_request_handler()  # close db connection
            sys.exit("Connection terminated")


def logout():
    time.sleep(1)
    after_request_handler()
    sys.exit("Logged out")


if __name__ == "__main__":
    before_request_handler()  # initialise db connection
    main(sys.argv[1:])
