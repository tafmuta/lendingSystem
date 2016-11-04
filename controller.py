# Controller
# handles borrowing
import uuid
from datetime import datetime
from datetime import timedelta
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


def Request(self, loan, duration, loan_amount):
    loan.Amount += loan
    deadline = datetime.now()+timedelta(days=duration)
    loan.Deadline = deadline
    id = uuid.uuid1()             # use the uuid module to get an unique loan id
    loan.loan_Id = id.bytes()     # store the loan in the database in bytes
    loan.save()
    print("Confirmed\n Your loan id is: %d", id.time_low)     # display the created loan id to the customer

