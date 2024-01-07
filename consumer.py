import json

import pika
import time


def consumer():
    # print("+" * 120)
    # print("+" * 120)
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue="email", durable=True)
    channel.queue_declare(queue="sms", durable=True)
    print(" [*] Waiting for messages. To exit press CTRL+C")

    def email_callback(ch, method, properties, body):
        message = json.loads(body)
        print(" [x] Received email message: %r" % message)

        time.sleep(1)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def sms_callback(ch, method, properties, body):
        message = json.loads(body)
        print(" [x] Received sms message: %r" % message)

        time.sleep(1)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="email", on_message_callback=email_callback)
    channel.basic_consume(queue="sms", on_message_callback=sms_callback)

    channel.start_consuming()


if __name__ == "__main__":
    consumer()
