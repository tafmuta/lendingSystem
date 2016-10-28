#! C:/Python35
# customer.py
# A Customer class of the lending system
# A customer can: Register himself
#                 Take a loan after his details have been verified
#                 Loans taken have a limit based on the customer's scoring

from Loan import Loan
from loanOfficer import loanOfficer
from Models import *

class Customer():

    def __init__(self, name=None, custId=None):
        self.cust_Id = custId
        self.Customer_Name = name
        self.loan = Loan()
        self.officer = loanOfficer()

    # Registers the customers and calls the loan Officer to verify the customer details
    def Register(self, name, Id_Num, Address):
        self.Customer_Name = name                         # customer name
        self.Id_Number = Id_Num                           # Customer's national Id number
        self.Address = Address                            # Customer's physical address
        self.officer.Verify(self.Customer_Name, self.Id_Number, self.Address)


    # asks for a loan
    def Borrow(self, Amount, Duration):
        try:
            # requesting for a loan
            self.loan.Request(Amount, Duration, self.get_custDetails(), self.officer.get_Score())
        except(ValueError):             # Loan.Request function raises and error in case it cant process the lona
            print("Cannot process your loan request at the moment ")
        finally:
            print("Thank you for banking with us!")

    # paying back the loan
    def pay(self, Amount, loan_Id):
        return Loan.Pay(Amount, loan_Id, self.get_custDetails())

    # gets the customer id
    def get_custDetails(self):
        return self.cust_Id