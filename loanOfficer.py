#! C:\Python35
# loanOfficer.py - loanOfficer class
# A loanOfficer manages customer registration (updates the db)
# He also scores customers

from Models import *
import controller
from utils import *
from peewee import *
import re
from uuid import *
from datetime import datetime


class loanOfficer():
    def __init__(self):
        try:
            self.login()
            Officer.get(Officer.password == self.passw)
            Officer.get(Officer.id == self.id)
            print "Login succesful!"
        except:
            raise ValueError("Invalid login details!")

        # self.login()

    def score_Customer(self, usr_id=None, score=None):
        usr_id = raw_input("Enter customer id: ")
        score = int(raw_input("Enter customer's score: "))
        usr = Customer.get(Customer.Customer_Id == usr_id)
        usr.Score = score
        usr.save()
    def list_unscored_customers(self): # lists all unscored customers
        cust_records = Customer.select()
        for cust in cust_records:
            print cust.Name,cust.Customer_Id,cust.Score


    def login(self):
        self.id  = raw_input("Enter user id: ")
        self.passw = raw_input("Enter your password: ")

    def send_batch_messages(self): # send batch messages
        pass

def Create_usr(Nme=None, Id_num=None, Add=None):
    Nme = raw_input("Enter your name: ")
    Id_num = raw_input("Enter your id number: ")
    Add = raw_input("Enter your address: ")
    try:
        # with db.atomic():
        encrypted_id, usr_id = generate_customerid(Nme)
        cust = Customer.create(Customer_Id = usr_id, National_id=Id_num, Name=Nme, Address=Add, )
        return "Your id is %d" % usr_id
    except IntegrityError as e:
        # `national_id` is a unique column, so a user with
        # this ID number exists already exists,
        # making it safe to call .get().
        return e.__repr__()

def create_admin():
    usr_nme = raw_input("Enter username: ")
    passw = raw_input("Enter password: ")
    Officer.create_or_get(id=usr_nme, password=passw)

def request_loan():
    try:
        cust_id = raw_input("Enter your customer id ").strip(" ")
        amount = int(raw_input("Enter amount you wish to borrow: "))
        days = raw_input(
            "Enter duration of the loan(number followed by type e.g 2 weeks): ").strip(" ")
        channel = raw_input(
            "Enter channel for loan disbursment(Mpesa or Airtel Money): ")
        myCust = Customer.get(Customer.Customer_Id == cust_id)
        name = myCust.Name
        if Customer.select(Customer.Score).where(Customer.Customer_Id == cust_id) >= amount:
            if channel.lower() == "mpesa":
                message = "[*] Sending %s %d via Mpesa" % (name,amount)
                print "[*] strating mpesa channel"
                emit(message=message, routing_key="Mpesa")
                recieve()
            else:
                message = "[*] Sending %s %d via Airtel Money" % (name, amount)
                print "[*] Starting Airtel Money Channel "
                emit(message=message, routing_key="AirtelMoney")
                recieve()
            type = "".join(re.findall(r'[A-za-z]+', days))
            days = int(re.findall(r'/d+', days))
            if type.lower() == "weeks":
                days *= 7
            elif type.lower() == "months":
                days *= (30)
            elif type.lower() == "years":
                days *= 365
            usr = Loan.select().join(Customer).\
                where(Customer.Customer_Id == cust_id)
            controller.Request(loan=usr, loan_amount=amount, duration=days, )
            # set a reminder to remind customer when payement date reaches
            secondsToDeadline = days * 24 * 60 * 60
            reminder(queue_name=name)  # send reminder
            receive_remider(secondsToDeadline,name)
        else:
            return "Inadequate score to take a loan"
        # message
    except:
        return "Make sure you are registered before asking for a loan"

if __name__ == "__main__":
    before_request_handler()
    # print Create_usr()
    print "%%**************%%%%"
    print request_loan()
    # officer = loanOfficer()
    # print "%%**************%%%%"
    # print officer.list_unscored_customers()
    # officer.score_Customer()
    # print "%%**************%%%%"
    # print officer.list_unscored_customers()

