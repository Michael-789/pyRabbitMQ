import pika
import sys


class RabbitMQHandler:
    def __init__(self):
        credentials = pika.PlainCredentials('vuser', 'pass')
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', virtual_host='vhost', credentials=credentials))
        self.channel = self.connection.channel()

    def recieve(self, exchanges=[], queues=[]):
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))
        # channel = connection.channel()
        binding_key = '#'
        queue_names = []
        for i in range(len(exchanges)):
            result = self.channel.queue_declare(queue=queues[i], exclusive=True)
            queue_names.append(result.method.queue)
            self.channel.queue_bind(
                exchange=exchanges[i], queue=queues[i], routing_key=binding_key)

        # result = self.channel.queue_declare(queue='LochmamFusedEntity', exclusive=True)
        # queue_name = result.method.queue
        # result1 = self.channel.queue_declare(queue='LochmamEntity', exclusive=True)
        # queue_name1 = result1.method.queue

        # self.channel.queue_bind(exchange='LcmFusedEntity', queue=queue_name, routing_key=binding_key)
        # self.channel.queue_bind(exchange='LcmEntity', queue=queue_name1, routing_key=binding_key)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print("Received [x] %r:%r" % (method.routing_key, body))
            # self.channel.stop_consuming()

        for queue_name in queue_names:
            self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()

    def recieve2(self):
        # connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))
        # channel = connection.channel()
        result = self.channel.queue_declare(queue='LochmamFusedEntity1', exclusive=True)
        queue_name = result.method.queue

        binding_key = 'debug'

        self.channel.queue_bind(exchange='LcmFusedEntity', queue=queue_name, routing_key='debug')

        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print("Received [x] %r:%r" % (method.routing_key, body))

        self.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()

    # def __del__(self):
