import pika
import sys

class RabbitMQHandler:
    def __init__(self):
        credentials = pika.PlainCredentials('vuser', 'pass')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', virtual_host='vhost', credentials=credentials))
        self.channel = self.connection.channel()


    def recieve(self):
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))
        # channel = connection.channel()
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue

        binding_key = 'entity.info'


        self.channel.queue_bind(exchange='topic_entity', queue=queue_name, routing_key=binding_key)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()