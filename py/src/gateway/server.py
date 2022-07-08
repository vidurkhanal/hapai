from flask import Flask, request
from flask_pymongo import PyMongo
import os
import pika
import json
import gridfs
from auth_svc import access
from auth import validate
from storage import util


server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal/:27017/videos"

mongo = PyMongo(server)

fs = gridfs.GridFS(mongo.db)

conn = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = conn.channel()


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

    if access['isAdmin']:
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file needed", 400

        for _, f in request.files.items():
            err = util.upload(f, fs, channel, access)

            if err:
                return err

        return "Success!", 200
    else:
        return "Not Authorized", 400


@server.route("/download", methods=["POST"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)