#!/bin/bash
# Resources: https://saurabhgujjar.medium.com/django-channels-with-daphne-gunicorn-and-nginx-on-digitalocean-all-in-one-guide-28625eead962

DIR=$(dirname "$0")
WEBUI="$DIR/webui/"
ENV="$DIR/env/bin"

USER="USERNAME"  # SET change to your username
IP_ADDRESS="IP_ADDRESS"  # SET change to your ip address

# Set environment variables (remove '#' to set a variable, or set them in your environment)
#export SECRET_KEY=""
#export IS_DEVELOPMENT=""
#export ALLOWED_HOSTS=""

#############################################

# Create and activate environment
python -m pip install --upgrade pip
sudo -H pip install virtualenv
virtualenv $DIR/env
source env/bin/activate

# Install dependencies
pip -m install -r docs/requirements.txt
deactivate
sudo apt-get install -y ngnix
sudo systemctl start nginx
sudo apt-get install -y ufw
sudo ufw enable

# Collect static files
source $ENV/activate
python $WEBUI/manage.py collectstatic --noinput
deactivate

# allow ports
sudo ufw allow 8000
sudo ufw allow 8001
sudo ufw allow 80
sudo ufw allow 'Nginx Full'

#############################################

# Configure Gunicorn
sudo touch /etc/systemd/system/gunicorn.service
# DEBUG sudo echo?
echo "
[Unit]
Description=gunicorn daemon
After=network.target
[Service]
User=$USER
Group=www-data
WorkingDirectory=$DIR
ExecStart=$ENV/gunicorn --access-logfile - --workers 1 --pythonpath $WEBUI --bind unix:$DIR.sock webui.wsgi:application
Restart=on-failure  # DEBUG
[Install]
WantedBy=multi-user.target" >> /etc/systemd/system/gunicorn.service

#############################################

# Configure Daphne
sudo touch /etc/systemd/system/daphne.service
# DEBUG sudo echo?
echo "
[Unit]
Description=WebSocket Daphne Service
After=network.target
[Service]
Type=simple
User=$USER
WorkingDirectory=$DIR
ExecStart=$ENV/python $ENV/daphne -b 0.0.0.0 -p 8001 webui.asgi:application
RestartSec=3s
Restart=on-failure
[Install]
WantedBy=multi-user.target" >> /etc/systemd/system/daphne.service

#############################################

# Configure Nginx
sudo touch /etc/nginx/sites-available/webui
# DEBUG sudo echo?
echo "
upstream channels-backend {
    server localhost:8001;
}
server {
    listen 80;
    server_name $IP_ADDRESS;

    location /static/ {
        alias $WEBUI/staticfiles/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$DIR.sock;
    }

    location /ws/ {
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect off;
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host \$server_name;
    }
}" >> /etc/nginx/sites-available/webui

sudo ln -s /etc/nginx/sites-available/webui /etc/nginx/sites-enabled

#############################################

# Start services
sudo systemctl daemon-reload

sudo systemctl start gunicorn.service
sudo systemctl start daphne.service
sudo systemctl restart nginx.service
sudo systemctl enable gunicorn.service
sudo systemctl enable daphne.service
sudo systemctl enable nginx.service