import os
import psycopg2
import bcrypt


conn = psycopg2.connect(
    host="localhost",
    database="minisrv",
    user=os.environ["DATABASE_USERNAME"],
    password=os.environ["DATABASE_PASSWORD"],
)

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users;")
cur.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
cur.execute(
    "CREATE TABLE users (id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,"
    "username varchar (255) UNIQUE NOT NULL,"
    "password varchar (255) NOT NULL,"
    "date_added date DEFAULT CURRENT_TIMESTAMP);"
)
hashed_pwd = bcrypt.hashpw(b"ssfsfsf", bcrypt.gensalt())
cur.execute(
    "INSERT INTO users (username, password)" "VALUES (%s, %s)",
    (
        "vidur@test1.co",
        hashed_pwd,
    ),
)

conn.commit()

cur.close()
conn.close()
