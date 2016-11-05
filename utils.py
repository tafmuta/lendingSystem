#! C:\Python35
# utils.py - contains functions to perform various utility functions
# generate customer Id
import re
import time
from uuid import *

import pika

from Models import *


def generate_customerid(usr_name):
    id = uuid3(NAMESPACE_DNS, usr_name)
    encrypted_id = id             # stored in the data base
    usr_ID = int(id.time_low)
    return encrypted_id, usr_ID

# send messages
def emit(message, routing_key):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))

    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs',
                             type='topic')

    channel.basic_publish(exchange='topic_logs',
                          routing_key=routing_key,
                          body=message,
                          )

    print("[x] sent %r" % message)

    connection.close()

# recieve messages
def recieve():
    binding_keys = ('Mpesa',  # Mpesa channel
                    'AirtelMoney',  # Airtel Money Channel
                    '#',  # bulk sms
                    '#.loan.reminder'  # loan reminder channel
                    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))

    channel = connection.channel()
    channel.exchange_declare(exchange='topic_logs',
                             type='topic')

    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue

    for binding_key in binding_keys:
        channel.queue_bind(exchange='topic_logs',
                           queue=queue_name, routing_key=binding_key)

    def callback(ch, method, properties, body):
        nums = int("".join(re.findall("\d+", body)))
        messg = "".join(re.findall("[A-Za-z!@#$%^^&*() ]", body))
        if nums:
            time.sleep(nums)
            try:
                Loan.get(Paid=False)
                return ("[*] %r" % method.routing_key, messg)
            except:
                pass
        return ("[*] %r" % method.routing_key, messg)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    recieve()
