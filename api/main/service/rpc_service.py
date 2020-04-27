import os
import threading

import amqpstorm
from amqpstorm import Message

class RpcClient(object):
    """Asynchronous Rpc client."""

    def __init__(self, url, rpc_queue):
        self.queue = {}
        self.url = url
        self.channel = None
        self.connection = None
        self.callback_queue = None
        self.listening_thread = None
        self.rpc_queue = rpc_queue
        self.open()

    def open(self):
        """Open Connection."""
        self.connection = amqpstorm.UriConnection(
            self.url
        )
        self.channel = self.connection.channel()
        self.channel.queue.declare(self.rpc_queue)
        result = self.channel.queue.declare(exclusive=True)
        self.callback_queue = result['queue']
        self.channel.basic.consume(self._on_response, no_ack=True,
                                   queue=self.callback_queue)
        self._create_process_thread()

    def _create_process_thread(self):
        """Create a thread responsible for consuming messages in response
         to RPC requests.
        """
        self.listening_thread  = threading.Thread(target=self._process_data_events)
        self.listening_thread.setDaemon(True)
        self.listening_thread.start()

    def _process_data_events(self):
        """Process Data Events using the Process Thread."""
        self.channel.start_consuming()

    def _on_response(self, message):
        """On Response store the message with the correlation id in a local
         dictionary.
        """
        self.queue[message.correlation_id] = message.body

    def send_request(self, payload):
        # Create the Message object.
        message = Message.create(self.channel, payload)
        message.reply_to = self.callback_queue

        # Create an entry in our local dictionary, using the automatically
        # generated correlation_id as our key.
        self.queue[message.correlation_id] = None

        # Publish the RPC request.
        message.publish(routing_key=self.rpc_queue)

        # Return the Unique ID used to identify the request.
        return message.correlation_id
    
    def close(self):
        self.listening_thread.join()
        self.connection.close()
    
def get_client():
    client = None
    rabbit_mq_url = os.getenv('RABBIT_MQ_URL')
    rabbit_mq_rpc_queue = os.getenv('RABBIT_MQ_QUEUE')
    if rabbit_mq_rpc_queue is None:
        rabbit_mq_rpc_queue = 'rpc_queue'
    if rabbit_mq_url:
        client = RpcClient(rabbit_mq_url, rabbit_mq_rpc_queue)
    return client