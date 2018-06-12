#!/bin/bash

echo "=> Installing npm modules"
cd /vagrant/frontend
CI=true npm install

echo "=> Configuring frontend"
cp /vagrant/vagrant/configs/fitoemanews.js /vagrant/frontend/src/config.js

echo "@ Frontend set up!"