from email import message
import pika
import json
import tempfile
import os
from bson.objectid import ObjectId
import moviepy.editor


def start(msg, fs_videos, fs_mp3, channel):
    msg = json.loads(msg)

    tf = tempfile.NamedTemporaryFile()

    out = fs_videos.get(ObjectId(msg["video_fid"]))

    tf.write(out.read())

    # create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    tf_path = tempfile.gettempdir() + f"/{msg['video_fid']}.mp3"
    audio.write_audiofile(tf_path)

    # save file to Mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3.put(data)
    f.close()
    os.remove(tf_path)

    message["mp3_field"] = str(fid)

    try:
        channel.basic_publish(
            exchane="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs_mp3.delete(fid)
        return "failed to publish the mp3,err: "+err
