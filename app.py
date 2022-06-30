import pika, os, signal, sys
from datetime import datetime

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

url = os.environ.get('AMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='hello') # Declare a queue
for x in range(600):
  channel.basic_publish(exchange='',
                  routing_key='hello',
                  body='Hello ' + str(x) + '<-')
  dateTimeObj = datetime.now()
  print(" [x] Sent Hello ->" + str(x) + " : "+ str(dateTimeObj))

def callback(ch, method, properties, body):
   dateTimeObj = datetime.now()
   print(" [x] Received " + str(body)+ " : "+ str(dateTimeObj))

channel.basic_consume('hello',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
