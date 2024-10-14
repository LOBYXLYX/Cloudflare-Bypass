import json
import httpx
import typing
import subprocess
from dataclasses import dataclass
from wb_base_data import wbBaseData


@dataclass
class CF_MetaData:
    domain: str
    clientRequest: typing.Union[typing.Any, httpx.Client]
    userAgent: typing.Optional[str]

    jsd_main_url: str

    def _get_s_parameter(self) -> tuple[typing.Optional[str], str]:
        r = self.clientRequest.get(self.domain + self.jsd_main_url, follow_redirects=True)
        html_site = r.text

        s_param = None
        cf_ray = r.headers['CF-RAY'].split('-')[0]

        for i,v in enumerate(html_site.split(',/')):
            if v.startswith('0.'):
                s_param = v.split('/,')[0]
                break
        return s_param, cf_ray

    def _get_sitekey_value(self):
        r = self.clientRequest.get(self.domain + self.jsd_main_url, follow_redirects=True).text
        spli1 = r.split("ah='")[1].split(',')

        for i, v in enumerate(spli1):
            if len(v) == 65:
                siteKey = v
                break
        return siteKey

    def cf_cookie_parse(self) -> tuple[str, typing.Optional[str], str]:
        base_data = wbBaseData(
            domain=self.domain.replace('https://', ''),
            useragent=self.userAgent
        )

        base_str = json.dumps(base_data, separators=(',', ':'))
        siteKey = self._get_sitekey_value()
        print('Site Key:', siteKey)

        result = subprocess.run(
            ['node', 'wb_encrypter.js', base_str, siteKey],
            capture_output=True,
            text=True
        )

        wb = result.stdout.strip()
        s, cf_ray = self._get_s_parameter()
        return wb, s, cf_ray


class CF_Solver(CF_MetaData):
    """
    Code Examples:
        - code 1:
            cf = CF_Solver('https://discord.com')
            cookie = cf.cookie() # return cf_clearance cookie


        - code 2:
            # Different cdn-cgi/challenge-platform URL 

            cf = CF_Solver(
                'https://www.support.kogama.com',
                jsd_main='/cdn-cgi/challenge-platform/h/b/scripts/jsd/62ec4f065604/main.js',
                jsd_request='/cdn-cgi/challenge-platform/h/b/jsd/r'
            )
            cookie = cf.cookie() # return cf_clearance cookie

        - code 3:
            import requests

            session = requests.Session()
            session.headers = {...}

            cf = CF_Solver(
                'https://discord.com',
                clientRequest=session
            )
            cookie = cf.cookie() # return cf_clearance cookie
    """

    def __init__(
        self, 
        domain: str, 
        *,
        clientRequest: typing.Any = None, 
        userAgent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        jsd_main : str = '/cdn-cgi/challenge-platform/scripts/jsd/main.js',
        jsd_request: str = '/cdn-cgi/challenge-platform/h/g/jsd/r'
    ):
        self.domain = domain
        self.client = clientRequest
        self.userAgent = userAgent
        self.jsd_main = jsd_main
        self.jsd_request = jsd_request

        if self.client is None:
            self.client = httpx.Client(
                headers={
                    'user-agent': self.userAgent,
                    'content-type': 'application/json',
                    'referer': self.domain + '/',
                    'origin': self.domain
                },
                timeout=10
            )

        self.cf_ray: typing.Optional[str] = None

        super().__init__(
            domain=self.domain,
            clientRequest=self.client, 
            userAgent=self.userAgent,
            jsd_main_url=self.jsd_main
        )

    def cookie(self):
        wb, s_param, self.cf_ray = self.cf_cookie_parse()
        payload = {
            'wb': wb,
            's': s_param
        }
        jsd = self.client.post(
            f'{self.domain}{self.jsd_request}/{self.cf_ray}',
            json=payload
        )
        return jsd.cookies['cf_clearance']


if __name__ == '__main__':
    cf = CF_Solver(
        'https://tempail.com',
        #jsd_main='/cdn-cgi/challenge-platform/h/b/scripts/jsd/62ec4f065604/main.js',
        #jsd_request='/cdn-cgi/challenge-platform/h/b/jsd/r'
    )
    a = cf.cookie()
    print(a)
