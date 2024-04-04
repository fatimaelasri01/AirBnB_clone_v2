#!/usr/bin/env bash

#installs nginx if not installed
if ! command -v nginx &> /dev/null; then
    apt-get -y update
    apt-get -y install nginx
fi

#create necessary dir if they don't exist
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

#create sym link
ln -sf /data/web_static/releases/test/ /data/web_static/current

#give ownership of /data/ to ubuntu user and group
chown -R ubuntu:ubuntu /data/

#update nginx configuration
sed -i '/hbnb_static/ { /alias/ { s/#//; } }' /etc/nginx/sites-available/default

#restart nginx
service nginx restart

exit 0
