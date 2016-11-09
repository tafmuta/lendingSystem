#! usr/bin/env/python2
#  loanOfficer.py - loanOfficer class
#  A loanOfficer manages customer registration (updates the db)
#  He also scores customers
from datetime import *

from Models import *
from utils import *


class loanOfficer():
    """Docstring for the loan officer"""

    def __init__(self, usr=None):
        try:
            self.create_admin(usr_name="Admin", passw="password")
        except:
            usr = raw_input("Enter your id: ")
            passw = raw_input("Enter your password: ")
            self.login(usr=usr, passw=passw)


        # self.login()

    def score_Customer(self, usr_id=None, score=None):  # Enables the loan officer score the customers
        usr_id = raw_input("Enter customer's National id Number: ")
        try:
            usr = Customer.get(Customer.National_id == usr_id)
        except:
            after_request_handler()
            print "Please provide a valid customer's national id!"
            sys.exit(1)
        score = int(raw_input("Enter customer's score: "))
        usr.Score = score
        print "Operation succesful!"
        usr.save()

    def list_unscored_customers(self): # lists all unscored customers
        cust_records = Customer.select()
        print "Name\t National id\t Score\t \n"
        for cust in cust_records:
            print "%s\t %d\t\t %d" % (cust.Name, cust.National_id, cust.Score)

    def login(self, usr=None, passw=None):  # handles login for the loan officer
        self.id = usr
        self.passw = passw
        try:
            Officer.get(id=usr, password=passw)
        except:
            after_request_handler()
            return "Invalid login details"

    def create_admin(self, usr_name=None, passw=None):  # creates a new system administrator
        if not usr_name and not passw:
            usr_nme = raw_input("Enter a username: ")
            passw = raw_input("Enter a password: ")
        Officer.create(id=usr_nme, password=passw)


    def send_bulk(self):  # Sending bulk sms
        message = raw_input("Enter message: ")
        topic = raw_input("Enter message category: ")
        emit(message=message, routing_key=topic)


# end of loanofficer class
# **********************************#
# Helper functions

def Create_usr(Nme=None, Id_num=None, Add=None):  # creates a new customer
    # get user details
    Nme = raw_input("Enter your name: ")
    Id_num = raw_input("Enter your id number: ")
    Add = raw_input("Enter your address: ")
    try:  # try creating the user
        with db.atomic():
            encrypted_id, usr_id = generate_customerid(str(Id_num))
            return Customer.create(Customer_Id=encrypted_id, National_id=Id_num, Name=Nme, Address=Add)
    except IntegrityError as e:  # except if a user with the same national id already exists
        # `national_id` is a unique column, so a user with
        # this ID number exists already exists,
        # making it safe to call .get().
        print "A customer with the same ID number exists. Try loging in instead"


def request_loan():  # allows customer to ask for a loan

        # get customer's details
        cust_id = raw_input("Enter your national ID number ").strip(" ")
        try:
            myCust = Customer.get(Customer.National_id == cust_id)
        except:
            after_request_handler()
            return "Please ensure you are registered before asking for a loan"

        name = myCust.Name
        amount = int(raw_input("Enter amount you wish to borrow: "))
        # check if customer's score is enough to take the specified loan
        if myCust.Score >= amount:
            duration = raw_input(
                "Enter duration of the loan(number followed by type e.g 2 weeks): ").strip(" ")
            channel = raw_input(
                "Enter channel for loan disbursment(Mpesa or Airtel Money): ")
            # create an mpesa channel
            if channel.lower() == "mpesa":
                message = "%s %d via Mpesa" % (name, amount)
                emit(message=message, routing_key="Mpesa")
            # create an airtel money channel
            else:
                message = "[*] %s %d via Airtel Money" % (name, amount)
                emit(message, routing_key="AirtelMoney")
            type = "".join(re.findall(r'[A-za-z]+', duration))
            days = int("".join(re.findall(r'\d+', duration)))
            # get number of days to the deadline
            if type.lower() == "weeks":
                days *= 7
            elif type.lower() == "months":
                days *= (30)
            elif type.lower() == "years":
                days *= 365

            # generate the loan id
            id = uuid1()
            deadline = datetime.now() + timedelta(days=int(days))
            Loan.create(loan_Id=id, customer=Customer.get(Customer.National_id == cust_id), Amount=amount,
                        paid=False, Deadline=deadline)
            # set a reminder and add it to queue to remind customer when payement date reaches
            secondsToDeadline = days * 24 * 60 * 60
            message = "Please repay your debt" + str(secondsToDeadline)
            keys = str(id) + "." + str(cust_id) + ".loan.reminder"
            emit(message=message, routing_key=keys)
        else:
            # customer doesnt have enough score to take a loan
            print "Inadequate score to take a loan"
