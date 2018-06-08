CREATE TABLE users
(
    id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    name varchar(64) NOT NULL,
    surname varchar(64) NOT NULL,
    email varchar(255) NOT NULL,
    password binary(60) NOT NULL,
    privileges int DEFAULT 1 COMMENT '1=pending'
);
CREATE UNIQUE INDEX users_email_uindex ON users (email);