#!/usr/bin/env bash

#check if script is run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

#install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

#create necessary directories if they don't exist
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

#create fake HTML file
web="<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>"
echo "$web" > /data/web_static/releases/test/index.html

#create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

#give ownership of /data/ to ubuntu user and group
chown -R ubuntu:ubuntu /data/

#update Nginx configuration
sed -i '/hbnb_static/ { /alias/ { s/#//; } }' /etc/nginx/sites-available/default

#restart Nginx
service nginx restart

exit 0

