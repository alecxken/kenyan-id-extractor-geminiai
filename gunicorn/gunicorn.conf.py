workers = 3
bind = "127.0.0.1:8000"
timeout = 120
worker_class = "sync"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"