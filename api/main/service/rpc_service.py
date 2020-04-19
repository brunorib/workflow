import pika
import uuid
import os

class RpcClient(object):

    def __init__(self, url):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(url))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, json):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(json))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

client = RpcClient(os.getenv('RABBIT_MQ_URL'))

def get_client():
    return client