import gridfs
from pymongo import MongoClient
import pika
import sys
import os
from convert import to_mp3


def main():
    client = MongoClient("mongodb+srv://admin:" + os.environ.get("MONGO_PWD") +
                         "@cluster0.mimv9.mongodb.net/?retryWrites=true&w=majority")
    db_videos = client.videos
    db_mp3s = client.mp3s

    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="beaver-01.rmq.cloudamqp.com", credentials=pika.PlainCredentials(username=os.environ.get("RABBIT_USER"), password=os.environ.get("RABBIT_PWD")), heartbeat=600,
            blocked_connection_timeout=300)
    )

    channel = connection.channel()

    def callbackFn(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print("CONVERTED...", flush=True)

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callbackFn
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
