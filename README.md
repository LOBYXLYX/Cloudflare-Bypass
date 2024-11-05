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

discord: lyxz2
