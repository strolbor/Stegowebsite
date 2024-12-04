# Stego App

## Gunicorn SSL

```bash
sudo -i
systemctl stop apache2

gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:80 app

gunicorn -b 0.0.0.0:8080 app
```

p