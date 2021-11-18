#!/bin/sh

# Setup mysql server
sudo apt update
sudo apt install -y mysql-server
sudo systemctl start mysql


# Install test requirements
pip3 install --upgrade pip
pip3 install -r requirements.txt -r test-requirements.txt

pytest --it
