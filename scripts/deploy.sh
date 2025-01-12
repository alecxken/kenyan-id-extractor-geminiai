# Contents of scripts/deploy.sh
#!/bin/bash
# Stop existing Gunicorn process if running
pkill gunicorn

# Start Gunicorn
cd /path/to/your/app
gunicorn --config gunicorn/gunicorn.conf.py main:app

# Contents of Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

EXPOSE 8000

CMD ["gunicorn", "--config", "gunicorn/gunicorn.conf.py", "main:app"]