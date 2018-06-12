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
    build-essential
    libffi-dev
    tcl
    gcc
    xvfb
    libgtk2.0-0
    libnotify-dev
    libgconf-2-4
    libnss3
    libxss1
    libasound2
)
apt-get install -q -y ${packageslist[@]}

echo "=> Installing pip"
cd /tmp
wget -q https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

echo "=> Installing virtualenv"
pip install virtualenv

echo "=> Installing nodejs"
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -q -y nodejs

echo "=> Installing redis"
cd /tmp
curl -Os http://download.redis.io/redis-stable.tar.gz
tar xzf redis-stable.tar.gz
cd redis-stable
make &> /dev/null
make install &> /dev/null
mkdir /etc/redis
cp /tmp/redis-stable/redis.conf /etc/redis
sed -i -e "s/supervised no/supervised systemd/" /etc/redis/redis.conf
sed -i -e "s,dir ./,dir /var/lib/redis," /etc/redis/redis.conf
cp /vagrant/vagrant/configs/redis.service /etc/systemd/system/redis.service
adduser --system --group --no-create-home redis
mkdir /var/lib/redis
chown redis:redis /var/lib/redis
chmod 770 /var/lib/redis
sudo systemctl start redis
sudo systemctl enable redis
sleep 5
redis-cli PING

echo "@ System bootstrap completed!"