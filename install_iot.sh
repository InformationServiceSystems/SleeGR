#!/bin/bash

#Please note: This script is just for usage with ubuntu 14.04 or newer!
#You also need to run the script as root
#
#This script should install mongodb and matplotlib with all needed dependancies.
#it also installs all needed python libs, so you should be able to run the server directely.

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo apt-get install matplotlib python3 python3-pip
sudo apt-get build-dep python-matplotlib
sudo service mongod start
git clone git@bitbucket.org:skorkmazISS/iot-final.git
cd iot-final
pip3 install -r requirements.txt
