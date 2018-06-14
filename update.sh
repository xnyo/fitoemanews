#!/bin/bash

set -e

echo "=> Updating backend"
cd /vagrant/backend
git pull origin master
~/.pyenv/bin/pip install -r requirements.txt
~/.pyenv/bin/pip install -r requirements-dev.txt

echo "=> Updating frontend"
cd /vagrant/frontend
git pull origin master
npm install

echo "@ Updated!"