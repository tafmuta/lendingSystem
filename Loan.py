#! C:/Python35
# Loan.Py - The Loan class of a lending system
# Loans Have a period weekly, monthly, yearly
# can be disbursed through various channels of customer's preference

from Models import *

class Loan():

    def Pay(self, Amount, Loan_Id, customer_ID):
        # get the customer's Loan amount from the database
        # subtract to get the new loan amount
        # if the remaining loan amount is zero delete the whole record from the DB
        # display a message to show the completion of the transaction
        pass

    def Request(self, Amount, Duration, customer_Id, Score):
        # get the customers loan score form the DB
        # if the loan score is less than the recommended score
        # Do not process the loan
        # else process the loan and display a confirmatory message
        pass
