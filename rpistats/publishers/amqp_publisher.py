from . import Publisher
import pika
import json

class AmqpPublisher:
    def __init__(self, host, queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.queue = queue

    async def publish(self, data):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue,
                                   body=json.dumps(data))
        print("Data published to AMQP queue")
