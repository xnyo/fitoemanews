#!/bin/bash

echo "=> Configuring nginx"
rm -rf /etc/nginx/sites-enabled/default
cp /vagrant/vagrant/configs/fitoemanews.nginx.conf /etc/nginx/conf.d/fitoemanews.conf
sudo nginx -t
sudo nginx -s reload

echo "@ nginx set up!"