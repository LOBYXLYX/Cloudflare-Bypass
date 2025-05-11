# Requirements

```
pip install -r requirements.txt
```

```
pip install javascript
```

# Example

```python
from aqua import CF_Solver

cf = CF_Solver('https://discord.com')
cookie = cf.cookie()
print(cookie)

# other
cf = CF_Solver('https://tempail.com')
cookie2 = cf.cookie()
print(cookie2)

# follow up requests
response = cf.client.get(url=url, timeout=10)
response = cf.client.post(url=url, data=data, json=json, timeout=10)

```

# Turnstile Reverse Engineering Progress

- Reversed challenge token:
  ![dev](https://github.com/LOBYXLYX/Cloudflare-Bypass/blob/main/images/20241107_171954.jpg)
  ![cons](https://github.com/LOBYXLYX/Cloudflare-Bypass/blob/main/images/20241107_172047.jpg)

- Challenge Request Reversed:
  ![ch](https://github.com/LOBYXLYX/Cloudflare-Bypass/blob/main/images/20241126_205308.jpg)

- small showcase

https://github.com/user-attachments/assets/4f81bdb8-bc57-4dbb-9a78-f4ef37f96644

discord: lobyx1

# Web server

Exposes the service as a webserver

## Run 

### Production
```bash
gunicorn -c gunicorn.config.py app:app
```

### Development
```bash
python3 app:app
```

## Sample call

```http request
POST http://localhost:1180/process
content-type: application/json

{
  "url": "https://unix.stackexchange.com",
  "proxy": "127.0.0.1:8080",
  "cookie_only": true,
  "insecure_skip_verify": true,
  "headers": {
    "header1": "value1"
   }
}
```

## More examples

`View example.http`

# Docker

## Build

```bash
docker build -t cfbypass .
```

## Run

```bash
docker run -it -p1180:1180 cfbypass
```

### Parameters

| Env var               | Description                   | Default |
|-----------------------|-------------------------------|---------|
| GUNICORN_WORKER_COUNT | Max gunicorn workers          | 8       |
| GUNICORN_THREADS      | Max gunicorn threads          | 8       |           
| GUNICORN_TIMEOUT      | Max time per request          | 60      |
| GUNICORN_BACKLOG      | Max requests to keep in queue | 16      |                       
