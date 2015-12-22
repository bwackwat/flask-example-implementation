#!/bin/bash

apt-get upgrade
apt-get update

apt-get install nginx

apt-get install python python-flask python-pip python-dev python-psycopg2
apt-get install postgresql postgresql-client postgis
apt-get install libpq-dev libffi-dev

pip install --upgrade cffi
pip install flask flask-bcrypt flask-sqlalchemy pyjwt sqlalchemy geoalchemy2 psycopg2

#passwd postgres
#ALTER USER "postgres" WITH PASSWORD 'aq12ws';
#CREATE EXTENSION postgis;

#chown -R www-data:www-data ./public

#openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt
