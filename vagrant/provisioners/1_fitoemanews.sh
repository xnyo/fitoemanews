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

echo "=> Installing requirements"
~/.pyenv/bin/pip install -r requirements.txt
~/.pyenv/bin/pip install -r requirements-dev.txt

echo "=> Creating database"
mysql -u root -proot -e "DROP DATABASE IF EXISTS fitoemanews; CREATE DATABASE fitoemanews;"

echo "=> Creating test database"
mysql -u root -proot -e "DROP DATABASE IF EXISTS fitoemanewstest; CREATE DATABASE fitoemanewstest;"

echo "=> Configuring fitoemanews"
cp /vagrant/vagrant/configs/fitoemanews.ini /vagrant/backend/settings.ini

echo "=> Running migrations and first scrape (this may take a while)"
~/.pyenv/bin/python fitoemanews.py scrape

echo "@ Backend set up!"