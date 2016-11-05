#! usr/bin/env/python2
# main.py - driver for the lending system

import getopt
import sys

from Models import *
from loanOfficer import *


def main(argv):
    if len(argv) < 2:
        print """usage: main.py [command] [option(s)]
               commands        options
               --admin -a      [loan officer's user name]                login to the system as an adiministrator
               --customer -c   N/A                                       login as a customer """
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "a:c", ["admin=", "customer="])
    except getopt.GetoptError:
        print """usage: main.py [command] [option(s)]
        commands        options
        --admin -a      [loan officer's user name]                login to the system as an adiministrator
        --customer -c   N/A                                       login as a customer """
    for opt, arg in opts:
        if opt in ("--admin", "-a"):
            before_request_handler()  # initialise db connection
            officer = loanOfficer(arg)
            choice = raw_input("press:\n"
                               "1. To score customer\n"
                               "2. To view customers details\n"
                               "3. To create a new admin\n"
                               "4. To logout"
                               )
            if choice == "1":
                try:
                    officer.score_Customer()
                except:
                    print "Request unsuccesful"
                finally:
                    logout()
            elif choice == "2":
                try:
                    officer.list_unscored_customers()
                except:
                    print "Request unsuccesfull"
                finally:
                    logout()
            elif choice == "3":
                try:
                    officer.create_admin()
                except:
                    print "Request unsuccesfull"
                finally:
                    logout()
            else:
                return logout()
        elif opt in ("--customer", "-c"):
            before_request_handler()  # initialise db connection
            choice = raw_input("Enter:\n"
                               "1. To request loan\n"
                               "2. To create an account\n"
                               "3. To quit\n"
                               )
            if choice == "1":
                try:
                    request_loan()
                except:
                    print "Request unsuccesfull"
                finally:
                    logout()
            elif choice == "2":
                try:
                    Create_usr()
                except:
                    print "Request unsuccesfull"
                finally:
                    logout()
            else:
                logout()
            after_request_handler()  # close db connection
            sys.exit("Connection terminated")


def logout():
    time.sleep(5)
    after_request_handler()
    sys.exit("Logged out")


if __name__ == "__main__":
    main(sys.argv[1:])
