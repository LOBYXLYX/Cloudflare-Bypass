url="https://stackoverflow.com/questions/57568571/"
url="https://www.google.com"
# url='https://solscan.io'
# url="https://tls.browserleaks.com/json"

import tls_client
s = tls_client.Session()
r = s.get(url)

from aqua import CF_Solver
cf = CF_Solver(url)
c = cf.cookie()
import sys
print("cf_clearance=" + c, file=sys.stderr)

from curl_cffi import requests
s = requests.Session(impersonate='chrome124')
s.cookies['cf_clearance'] = c
r = s.get(url)
print(r.content)


