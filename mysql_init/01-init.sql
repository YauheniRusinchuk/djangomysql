
CREATE DATABASE IF NOT EXISTS django_db;


USE django_db;


CREATE USER IF NOT EXISTS 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON django_db.* TO 'user'@'%';
FLUSH PRIVILEGES; 