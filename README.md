# Stego App

## Gunicorn SSL

```bash
gunicorn --certfile cert.pem --keyfile key.pem -b 0.0.0.0:8000 app

gunicorn -b 0.0.0.0:8000 app
```

