import pika
import json

from models import User, Post, connect
from mongoengine.queryset.visitor import Q


credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="task_exchange", exchange_type="direct")
channel.queue_declare(queue="email", durable=True)
channel.queue_declare(queue="sms", durable=True)
channel.queue_bind(exchange="task_exchange", queue="email", routing_key="email")
channel.queue_bind(exchange="task_exchange", queue="sms", routing_key="sms")


# Qoute.objects(author__icontains=author.id)
def producer():
    #print("*" * 120)
    #print("*" * 120)
    for message in Post.objects:
        user = User.objects(id=str(message.author.id)).first()
        if user.channel == "email":
            data = {
                "email": user.email,
                "user": user.fullname,
                "user_id": str(message.author.id),
                "text": message.title,
            }
            body = json.dumps(data)
            # print("::::", data, f"\n", body)
            channel.basic_publish(
                exchange="task_exchange",
                routing_key="email",
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
        elif user.channel == "phone":
            data = {
                "phone": user.phone,
                "user": user.fullname,
                "user_id": str(message.author.id),
                "text": message.title,
            }
            body = json.dumps(data)
            # print("::::", data, f"\n", body)
            channel.basic_publish(
                exchange="task_exchange",
                routing_key="sms",
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
        user.flag = True
        user.save()
    connection.close()


if __name__ == "__main__":
    producer()
