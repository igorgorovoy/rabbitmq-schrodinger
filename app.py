import pika, os, signal, sys
from datetime import datetime

def signal_handler(signal, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

url = os.environ.get('AMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='q1') # Declare a queue
for x in range(100000000):
  channel.basic_publish(exchange='',
                  routing_key='q1',
                  body='ping ' + str(x) + '*')
  dateTimeObj = datetime.now()
  print(" [x] ping ->" + str(x) + " : "+ str(dateTimeObj))

def callback(ch, method, properties, body):
   dateTimeObj = datetime.now()
   print(" [x] pong " + str(body)+ " : "+ str(dateTimeObj))

channel.basic_consume('q2',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()
