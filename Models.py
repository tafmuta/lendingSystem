#! usr/bin/python2
# Models.py - contains database models for the lending system
# Loan - Contains details of the customer loans related to the Customer's model
# through a one is to many relationship
# Customer - Contains customer's details
# Officer - Stores the loan officer details i.e password and user id

from datetime import datetime

from peewee import *  # A pyhton orm
from playhouse.sqlite_ext import SqliteExtDatabase

# define my databse
db = SqliteExtDatabase('my_app.db', journal_mode='WAL')

class baseModel(Model):
    class Meta:
        database = db


class Customer(baseModel):
    Name = CharField(default='Your name')
    Address = CharField(default='Address')
    National_id = IntegerField(default=00000000)
    Customer_Id = CharField(unique=True, primary_key=True)
    Score = IntegerField(default=0)


class Loan(baseModel):
    Deadline = DateField(default=datetime.now())
    customer = ForeignKeyField(Customer, related_name='loans')
    Amount = IntegerField(default=0)
    loan_Id = IntegerField(unique=True, primary_key=True)
    paid = BooleanField()

class Officer(baseModel):
    id = CharField(default="Admin")
    password = CharField(default="password")

def before_request_handler():
    db.connect()
    db.create_tables([Loan, Customer, Officer], safe=True)


def after_request_handler():
    db.close()
