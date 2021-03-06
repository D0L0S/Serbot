-------------------------------------------------------------------
-- Serbot DB v0.1                                                --
-------------------------------------------------------------------
CREATE USER 'serbot'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'serbot'@'localhost' WITH GRANT OPTION;
CREATE DATABASE serbot;
USE serbot;
CREATE TABLE clients (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(20), ip_address VARCHAR(30), os VARCHAR(30), active VARCHAR(30));
CREATE TABLE users (id INT PRIMARY KEY AUTO_INCREMENT, first_name VARCHAR(20), last_name VARCHAR(20), email VARCHAR(30), client_id INT(10));
CREATE TABLE attacks (id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(20), os VARCHAR(20), script_location VARCHAR(30))
