-------------------------------------------------------------------
-- Serbot DB v0.1                                                --
-------------------------------------------------------------------
CREATE DATABASE serbot;
USE serbot;
CREATE TABLE clients (id INT, name VARCHAR(20), ip_address VARCHAR(30), os VARCHAR(30), status VARCHAR(30));
CREATE TABLE users (id INT, first_name VARCHAR(20), last_name VARCHAR(20), email VARCHAR(30), client_id INT(10));
