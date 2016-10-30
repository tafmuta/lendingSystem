#! C:\Python35
# utils.py - contains functions to perform various utility functions
# generate customer Id

from uuid import UUID

def generate_CustomerId(usr_name):
    id = UUID(NAMESPACE_DNS, usr_name)
    encrypted_id = id.bytes             # stored in the data base
    usr_ID = int(id.time_low)
    return usr_ID