#! C:\Python35
# utils.py - contains functions to perform various utility functions
# generate customer Id
import pika
from uuid import *
from datetime import datetime

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

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
    binding_keys = ['Mpesa', 'AirtelMoney']
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
        print ("[*] %r" % body, method)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print('[*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# initialise a reminder messages
def reminder(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    message = "Dear customer please repay your loan to continue enjoying our services!"
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))
    print(" [x] Sent %r" % message)
    connection.close()

# recieve a reminder message and schedule its execution
def receive_remider(duration, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        time.sleep(duration)
        print(" %r " % body)        # return the message sent when deadline reaches
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback,
                          queue=queue_name)

    channel.start_consuming()