# Requirements
- Python 3.11.8+
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
### Reversing challenge token:
![devt](https://github.com/LOBYXLYX/Cloudflare-Bypass/blob/main/20241107_171954.jpg)
![cons](https://github.com/LOBYXLYX/Cloudflare-Bypass/blob/main/20241107_172047.jpg)

discord: lyxz2
