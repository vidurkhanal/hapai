from datetime import datetime, timedelta

import os
import bcrypt
from flask import Flask, request
import jwt
import psycopg2

# INIT A FLASK APP
server = Flask(__name__)

# DB INIT AND CONFIGS
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="minisrv",
        user=os.environ["DB_USERNAME"],
        password=os.environ["DB_PASSWORD"],
    )
    return conn


# JWTS
def createJWT(unhashed_username, key, hasSpecialPrivileges):
    return jwt.encode(
        {
            "username": unhashed_username,
            "exp": datetime.now(tz=datetime.utc) + timedelta(days=1),
            "iat": datetime.utcnow(),
            "isAdmin": hasSpecialPrivileges,
        },
        key,
        algorithm="HS256",
    )


# ROUTES
@server.route("/", methods=["GET"])
def home():
    return "<h1>Hello World</h1>"


# ROUTES___AUTH
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    cur = get_db_connection().cursor()
    res = cur.execute(
        "SELECT email,password from users WHERE email=%s", (auth.username)
    )
    if res:
        data = cur.fetchone()
        email = data[0]
        password = data[1]

        if auth.username != email or bcrypt.checkpw(auth.password, password):
            return "invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_KEY"), True)
    else:
        return "No user found with such email", 401


# ROUTES___APIVALIDATORS
@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        return "Missing credentials", 401
    encoded_jwt = encoded_jwt.split(" ")[1]
    decoded = ""
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_KEY"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 401

    return decoded


# START THE APP
if __name__ == "__main__":
    server.run("0.0.0.0", 5050)
