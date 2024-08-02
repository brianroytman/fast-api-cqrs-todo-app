import aio_pika
import os

class RabbitMQService:
    def __init__(self):
        self.rabbitmq_url = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')
        self.connection = None

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
            return self.connection
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def close_connection(self):
        if self.connection:
            await self.connection.close()

    async def publish_message(self, queue_name, message_body):
        if not self.connection:
            raise RuntimeError("Not connected to RabbitMQ")
        async with self.connection.channel() as channel:
            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key=queue_name
            )

    async def consume_message(self, queue_name, callback):
        if not self.connection:
            raise RuntimeError("Not connected to RabbitMQ")
        async with self.connection.channel() as channel:
            queue = await channel.declare_queue(queue_name)
            await queue.consume(callback)
