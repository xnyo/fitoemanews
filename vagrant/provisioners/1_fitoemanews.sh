#!/bin/bash

cd /vagrant/backend

if [ -d ~/.pyenv ] &&  [ ! -f ~/.pyenv/bin/python ]; then
    echo "Broken virtualenv detected. Removing and recreating it"
    rm -rf ~/.pyenv
fi

if [ ! -d ~/.pyenv ]; then
    echo "=> Initializing virtual environment"
    virtualenv -p $(which python3) ~/.pyenv -q
else
    echo "=> Virtualenv already exists! Virtualenv creation skipped."
fi

echo "=> Installing dependencies"
~/.pyenv/bin/pip install -r requirements.txt

echo "=> Creating database"
mysql -u root -proot -e "DROP DATABASE IF EXISTS fitoemanews; CREATE DATABASE fitoemanews;"

echo "=> Configuring fitoemanews"
cp /vagrant/vagrant/configs/fitoemanews.ini /vagrant/backend/settings.ini

# echo "=> Running migrations"
# ~/.pyenv/bin/python poc.py migrate