from peewee import *
from _datetime import datetime
from playhouse.sqlite_ext import SqliteExtDatabase

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
    loan_Id = CharField(unique=True, primary_key=True)
    paid = BooleanField()


def before_request_handler():
    db.connect()
    db.create_tables([Loan, Customer], safe=True)

def after_request_handler():
    db.close()
    
