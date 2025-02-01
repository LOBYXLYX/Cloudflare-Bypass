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


discord: