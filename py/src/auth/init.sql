DROP DATABASE IF EXISTS minisrv;


CREATE DATABASE minisrv;


SET SCHEMA 'minisrv';


CREATE TABLE USER(id serial PRIMARY KEY,
                                    email VARCHAR(255) NOT NULL,
                                                       password VARCHAR(255) NOT NULL);


INSERT INTO USER(email, password)
VALUES ("test.test.com",
        "test123");