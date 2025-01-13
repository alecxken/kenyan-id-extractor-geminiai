#!/bin/bash

# Set variables
APP_DIR="/app"
VENV_DIR="$APP_DIR/venv"
GUNICORN_SERVICE="flaskapp"
NGINX_CONFIG="flaskapp"
PORT=8000

# Ensure the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit
fi

# Update and install dependencies
echo "Updating system and installing dependencies..."
sudo apt update && sudo apt install -y python3 python3-venv python3-pip nginx

# Navigate to the app directory
if [ ! -d "$APP_DIR" ]; then
  echo "Error: Application directory $APP_DIR does not exist."
  exit 1
fi
cd $APP_DIR

# Set up Python virtual environment
echo "Setting up virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install flask gunicorn

# Create Gunicorn systemd service
echo "Creating Gunicorn systemd service..."
cat <<EOL > /etc/systemd/system/$GUNICORN_SERVICE.service
[Unit]
Description=Gunicorn instance to serve Flask app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
ExecStart=$VENV_DIR/bin/gunicorn --workers 3 --bind unix:$APP_DIR/$GUNICORN_SERVICE.sock main:app

[Install]
WantedBy=multi-user.target
EOL

# Start and enable Gunicorn service
echo "Starting and enabling Gunicorn service..."
systemctl start $GUNICORN_SERVICE
systemctl enable $GUNICORN_SERVICE

# Create Nginx configuration
echo "Configuring Nginx..."
cat <<EOL > /etc/nginx/sites-available/$NGINX_CONFIG
server {
    listen $PORT;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/$GUNICORN_SERVICE.sock;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOL

# Enable Nginx configuration
echo "Enabling Nginx configuration..."
ln -sf /etc/nginx/sites-available/$NGINX_CONFIG /etc/nginx/sites-enabled
nginx -t && systemctl restart nginx

# Adjust firewall
if command -v ufw &>/dev/null; then
  echo "Allowing traffic on port $PORT..."
  ufw allow $PORT
fi

# Print success message
echo "Deployment completed successfully! Visit http://<your-server-ip>:$PORT to view your app."
