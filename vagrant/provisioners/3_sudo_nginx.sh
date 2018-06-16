#!/bin/bash

echo "=> Configuring nginx"
rm -rf /etc/nginx/sites-enabled/default
cp /vagrant/vagrant/configs/fitoemanews.nginx.conf /etc/nginx/conf.d/fitoemanews.conf
sed -i -e "s/sendfile on/sendfile off/" /etc/nginx/nginx.conf
sudo nginx -t
sudo nginx -s reload

echo "@ nginx set up!"