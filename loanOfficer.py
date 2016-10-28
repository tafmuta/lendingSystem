#! C:\Python35
# loanOfficer.py - loanOfficer class
# A loanOfficer manages customer registration (updates the db)
# He also scores customers
# Interface.py
from Models import *
from Customer import *
from Loan import *

from Models import *

class loanOfficer():
    def __init__(self):
        before_request_handler()        # connect to the db

    def get_Score(self):
        pass

    def Verify(self, Nme, Id_num, Add):
        try:
            with db.atomic():
                return Customer.create(National_id=id_num, Name = Name, Address = Add)
        except peewee.IntegrityError:
            # `national_id` is a unique column, so a user with this ID number exists already exists,
            # making it safe to call .get().
            return User.get(User.username == username)