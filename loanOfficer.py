#! usr/bin/env/python2
#  loanOfficer.py - loanOfficer class
#  A loanOfficer manages customer registration (updates the db)
#  He also scores customers
import re
from datetime import *

from peewee import *

from utils import *


class loanOfficer():
    """Docstring for the loan officer"""

    def __init__(self, usr=None):
        try:
            self.login(usr=usr)
            Officer.get(Officer.password == self.passw)
            Officer.get(Officer.id == self.id)
            print "Login succesful!"
        except:
            raise ValueError("Invalid login details!")

        # self.login()

    def score_Customer(self, usr_id=None, score=None):  # Enables the loan officer score the customers
        usr_id = raw_input("Enter customer id: ")
        score = int(raw_input("Enter customer's score: "))
        usr = Customer.get(Customer.Customer_Id == usr_id)
        usr.Score = score
        usr.save()

    def list_unscored_customers(self): # lists all unscored customers
        cust_records = Customer.select()
        for cust in cust_records:
            print cust.Name,cust.Customer_Id,cust.Score

    def login(self, usr=None):  # handles login for the loan officer
        self.id = usr
        self.passw = raw_input("Enter your password: ")

    def create_admin(self):  # creates a new system administrator
        usr_nme = raw_input("Enter username: ")
        passw = raw_input("Enter password: ")
        Officer.create_or_get(id=usr_nme, password=passw)

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
            encrypted_id, usr_id = generate_customerid(Nme)
            Customer.create(Customer_Id=usr_id, National_id=Id_num, Name=Nme, Address=Add, )
            return "Your id is %d" % usr_id
    except IntegrityError as e:  # except if a user with the same national id already exists
        # `national_id` is a unique column, so a user with
        # this ID number exists already exists,
        # making it safe to call .get().
        return e.__repr__()


def request_loan():  # allows customer to ask for a loan
    try:
        # get customer's details
        cust_id = raw_input("Enter your customer id ").strip(" ")
        amount = int(raw_input("Enter amount you wish to borrow: "))
        duration = raw_input(
            "Enter duration of the loan(number followed by type e.g 2 weeks): ").strip(" ")
        channel = raw_input(
            "Enter channel for loan disbursment(Mpesa or Airtel Money): ")
        myCust = Customer.get(Customer.Customer_Id == cust_id)
        name = myCust.Name

        # check if customer's score is enough to take the specified loan
        if Customer.select(Customer.Score).where(Customer.Customer_Id == cust_id) >= amount:
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
            id = int(uuid.uuid1().time_low)
            deadline = datetime.now() + timedelta(days=int(days))
            Loan.create(loan_Id=id, customer=Customer.get(Customer.Customer_Id == cust_id), Amount=amount,
                        paid=False, Deadline=deadline)
            # set a reminder and add it to queue to remind customer when payement date reaches
            secondsToDeadline = days * 24 * 60 * 60
            message = "Please repay your debt" + str(secondsToDeadline)
            keys = str(id) + "." + str(cust_id) + ".loan.reminder"
            emit(message=message, routing_key=keys)
        else:
            # customer doesnt have enough score to take a loan
            return "Inadequate score to take a loan"
        # message
    except:
        return "Sorry we can not complete your loan requests at the moment"
