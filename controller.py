# Controller
# handles borrowing
import uuid
from datetime import datetime
import getopt
# TODO registrations


def Pay(self, Amount, loan):
    # get the customer's Loan amount from the database
    if loan.Amount == Amount:
        loan.Amount = 0
        loan.save()
        return "Loan fully paid"
    else:
        loan.Amount -= Amount
        loan.save()


def Request(self, loan, month=0, days=0, year=0, weeks=0):
    # check if the customer's score is okay
    if not loan.customer.Score >= 0.5:
        return "Inadequate score to take a loan"
    # TODO update the deadline and loan_Id
    else:
        loan.Amount += loan
        today = datetime.now()
        fMonth = today.month + month
        fday = today.day + days
        fyear = today.year + year
        ndate = datetime.date()
        loan.Deadline = nDate
        id = uuid.uuid1()
        loan.loan_Id = id.bytes()
        loan.save()
        print("Confirmed\n Your loan id is: %d", id.time_low)


def main(args):
    # TODO register customer
    # TODO ask for a loan
    # TODO pay loan
    # TODO get a list of loans
