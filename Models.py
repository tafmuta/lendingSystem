from peewee import *
import uuid
from _datetime import datetime
from playhouse.sqlite_ext import SqliteExtDatabase

# define my databse
db = SqliteExtDatabase('my_app.db', journal_mode='WAL')

# custom class for UUID


class UUIDField(Field):
    db_field = 'uuid'

    def db_value(self, value):
        return str(value)  # convert UUID to str

    def python_value(self, value):
        return uuid.UUID(value)  # convert str to UUID


class baseModel(Model):
    class Meta:
        database = db


class Customer(baseModel):
    Name = CharField(default='Your name')
    Address = CharField(default='Address')
    National_id = IntegerField(default=00000000)
    Customer_Id = UUIDField(unique=True, primary_key=True)
    Score = IntegerField(default=0.5)


class Loan(baseModel):
    Deadline = DateField(default=datetime.now())
    customer = ForeignKeyField(Customer, related_name='loans')
    Amount = IntegerField(default=0)
    loan_Id = UUIDField(unique=True, primary_key=True)
    paid = BooleanField()


def before_request_handler():
    db.connect()
    db.create_tables([Loan, Customer], safe=True)


def after_request_handler():
    db.close()
