# Update system and install dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev nginx

# Create directory for Gunicorn logs
sudo mkdir -p /var/log/gunicorn
sudo chown -R ubuntu:ubuntu /var/log/gunicorn

# Install Python dependencies
cd ./app
pip3 install -r requirements.txt

# Copy Nginx configuration
sudo cp nginx/flask_app.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/flask_app.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx