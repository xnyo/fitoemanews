#!/bin/bash

set -e

echo "@ Bootstrapping fitoemanews development environment"
echo "@ Using $(lsb_release -ircs | tr "\n" " ")"

if [ "$EUID" -ne 0 ]; then
    echo "bootstrap.sh must be run as root."
    exit -1
fi

echo "=> Installing MariaDB key"
apt-get update -qq
apt-get install -qq -y software-properties-common
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
sudo add-apt-repository "deb [arch=amd64,i386] http://mariadb.mirror.triple-it.nl/repo/10.2/ubuntu $(lsb_release -sc) main"

echo "=> Updating packages list"
apt-get update -qq

echo "=> Preparing mysql root password (for non-interactive mariadb installation)"
export DEBIAN_FRONTEND=noninteractive
sudo debconf-set-selections <<< 'mariadb-server-10.2 mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mariadb-server-10.2 mysql-server/root_password_again password root'

echo "=> Installing required packages"
packageslist=(
    git
    nginx
    mariadb-server
    python3.6
    python3.6-dev
)
apt-get install -q -y ${packageslist[@]}

echo "=> Installing pip"
cd /tmp
wget -q https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

echo "=> Installing virtualenv"
pip install virtualenv

echo "@ System bootstrap completed!"