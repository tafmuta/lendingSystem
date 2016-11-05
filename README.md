# lendingSystem
System built in Python to handle customer loan transactions
comaptible with python 2.* and previous versions

usage:
main.py [command] [option(s)]
commands        options
--admin -a      [loan officer's user name]                login to the system as an adiministrator

--customer -c                                              login as a customer

setup:
in the terminal:
run $ pip install -r requirements.txt
open a new terminal
run $ python utils.py    - this starts the message receiver
on another terminal
run $ python main.py [command] [option]

assumptions:
The user has python 2.* or any previous version installed in the system if not downloand it at www.python.org/downloads

defaultpasswords for admin are:
id = Admin
password = password