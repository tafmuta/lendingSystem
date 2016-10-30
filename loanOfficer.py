#! C:\Python35
# loanOfficer.py - loanOfficer class
# A loanOfficer manages customer registration (updates the db)
# He also scores customers
# Interface.py
from Models import *
import controller
import utils
from peewee import *


class loanOfficer():
    def __init__(self):
        before_request_handler()        # connect to the db

    def score_Customer(self, usr_id, score):
        usr = Customer.select().where(Customer.Customer_Id == usr_id)
        usr.Score = score
        usr.save()

    # TODO test this logic
    def get_Score(self, usr_id):
        return Customer.get_id()

    def Create_usr(self, Nme, Id_num, Add):
        try:
            with db.atomic():
                usr_id = utils.generate_CustomerId(Nme)
                cust = Customer.create(
                    National_id=Id_num, Name=Nme, Address=Add, )
                cust.Customer_Id = usr_id
                cust.save()
                return cust
        except IntegrityError:
            # `national_id` is a unique column, so a user with
            # this ID number exists already exists,
            # making it safe to call .get().
            return Customer.select().where(Customer.National_id == id_num)

    def pay_Loan(self, Amount, loan_id):
        usr = Loan.select().join(Customer).where(loan_Id=loan_id)
        controller.Pay(Amount=Amount, loan=usr)

    def request_loan(customerid, ):
        try:
            usr = Loan.select().join(Customer).\
                where(Customer.Customer_Id == customerid)
            return ("Please pay your outstanding \
                balance to be able to borrow!")
        except:
            usr = Loan.create(customer = Customer.select().where(Customer_Id = customerid))
            controller.Request(loan=usr, )