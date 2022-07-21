import pika
import sys
import os
from send import email


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            "rabbitmq", heartbeat=600,
            blocked_connection_timeout=300)
    )

    channel = connection.channel()

    def callbackFn(ch, method, properties, body):
        err = email.notify(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"), on_message_callback=callbackFn
    )

    print("WAITING  FOR MESSAGES...", flush=True)
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("EXITING THE CONSUMER SERVICE...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
