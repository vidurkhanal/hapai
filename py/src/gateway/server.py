from flask import Flask, request, send_file
from flask_pymongo import MongoClient
import os
import pika
import json
import gridfs
from auth_svc import access
from auth import validate
from storage import util
from bson.objectid import ObjectId


server = Flask(__name__)
client = MongoClient(
    "mongodb+srv://admin:" + os.environ.get("MONGO_PWD") + "@cluster0.mimv9.mongodb.net/?retryWrites=true&w=majority")
video_db = client.videos
audio_db = client.mp3s


# NEED TO TAKE A LOOK AT DB STRINGS
videos_fs = gridfs.GridFS(video_db)
audios_fs = gridfs.GridFS(audio_db)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        "rabbitmq", heartbeat=600,
        blocked_connection_timeout=300)
)
channel = connection.channel()


@server.route("/", methods=["GET"])
def home():
    return "<h1>Hello World"


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    access = json.loads(access)

    if err:
        return err

    if access['isAdmin']:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file needed", 400
        # POSSIBLE ERROR
        for _, f in request.files.items():
            err = util.upload(f, videos_fs, channel, access)

            if err:
                return err

        return "Success!", 200
    else:
        return "Not Authorized", 400


@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)
    access = json.loads(access)

    if err:
        return err

    if access['isAdmin']:
        fid_string = request.args.get("fid")
        if not fid_string:
            return "FID is required...", 400
        try:
            out = audios_fs.get(ObjectId(fid_string))
            return send_file(out, download_name=f'{fid_string}.mp3')
        except Exception as err:
            print(err, flush=True)
            return "internal server error", 500


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)
