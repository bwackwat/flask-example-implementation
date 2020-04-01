#!/usr/bin/bash

# Exit on error and print lines.
set -eux

# Useful prerequisites.
sudo apt-get -y update
sudo apt install -y ntpdate nfs-common mysql-client php7.2 php-mysql

# Prepare Docker.
sudo apt-get remove -y docker docker-engine docker.io
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce

# Images to use.
sudo docker image pull php:7.3-fpm-alpine
sudo docker image pull jlesage/nginx-proxy-manager

# WP Cli.
sudo curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
sudo chmod +x wp-cli.phar
sudo mv wp-cli.phar /usr/local/bin/wp

# Gluster FS
sudo add-apt-repository -y ppa:gluster/glusterfs-7
sudo apt-get update
sudo apt-get -y install glusterfs-client

# Good stuff.
sudo apt-get -y install openssh-server vim wget certbot

# Docker compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


pip install --upgrade cffi
pip install flask flask-bcrypt flask-sqlalchemy pyjwt sqlalchemy geoalchemy2 psycopg2

#passwd postgres
#ALTER USER "postgres" WITH PASSWORD 'aq12ws';
#CREATE EXTENSION postgis;

#chown -R www-data:www-data ./public

#openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt
