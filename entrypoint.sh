#!/bin/bash
# add additional dependencies required for your solution here.
# for example:
# pip3 install mysql-client

apt-get update && apt-get -y install sudo
sudo apt-get install -y python3-pip python-dev libmysqlclient-dev
pip install mysqlclient

sleep infinity
