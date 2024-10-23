import time
import sys
import types
import json
import httpx
import typing
import random
import requests as cf_captcha_req
import subprocess

from dataclasses import dataclass
from wb_base_data import wbBaseData
from interactive_data import parse_cf_params, CF_Interactive

@dataclass
class CF_MetaData:
    domain: str
    clientRequest: typing.Union[typing.Any, httpx.Client]
    userAgent: typing.Optional[str]

    jsd_main_url: str
    _domain_parsed: typing.Optional[str] = None

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

    def _get_sitekey_value(self) -> tuple[str, str]:
        r = self.clientRequest.get(self.domain + self.jsd_main_url, follow_redirects=True).text
        spli1 = r.split("ah='")[1].split(',')

        func_g = r.split("'g'")[2].split("},'")[0].split('1.')

        wb_float_gens = ''

        for i, v in enumerate(func_g):
            if v[:2].isnumeric() or v[:1].isnumeric():
                parsed_length = 2 if v[:2].isnumeric() else 1
                wb_float_gens += '1.' + v[:parsed_length] + ','

            if v[:3] == '1|1' and (v[:4].split('|')[1].isnumeric() or v[:5].split('|')[1].isnumeric()):

                parsed_length = 4 if v[:4].split('|')[1].isnumeric() else 5
                wb_float_gens += '1.' + v[:parsed_length].split('|')[1] + ','

        while not len(wb_float_gens.split(',')) > 8:
            wb_float_gens += str(round(random.uniform(1, 1.99), random.randint(1, 2))) + ','

        wb_float_gens = wb_float_gens[:len(wb_float_gens) - 1]

        for i, v in enumerate(spli1):
            if len(v) == 65:
                siteKey = v
                break
        return siteKey, wb_float_gens # convert str to list

    def _get_cf_ray(self):
        r = self.clientRequest.get(self.domain).headers
        return r['CF-RAY'].split('-')[0]

    def cf_cookie_parse(self) -> tuple[str, typing.Optional[str], str]:
        base_data = wbBaseData(
            domain=self.domain.replace('https://', ''),
            useragent=self.userAgent
        )

        base_str = json.dumps(base_data, separators=(',', ':'))
        siteKey, wb_floats = self._get_sitekey_value()

        result = subprocess.run(
            ['node', 'wb_encoder.js', base_str, siteKey, wb_floats],
            capture_output=True,
            text=True
        )

        wb = result.stdout.strip()
        s, cf_ray = self._get_s_parameter()
        return wb, s, cf_ray

    def cf_orchestrate_js(self, auto_mode=False):
        self._domain_parsed = 'https://' + self.domain.split('/')[2] if len(self.domain.split('/')) > 3 else self.domain
        cf_ray = self._get_cf_ray()
        print(cf_ray)
    
        self.clientRequest.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
            'cache-control': 'max-age=0',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1'
        })
        params = {
            'ray': cf_ray,
        }
        if auto_mode:
            params['lang'] = 'auto'

        chl = self.clientRequest.get(
            f'{self._domain_parsed}/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1',
            params=params
        )
        return chl.text

    def parse_orchestrate_params(self, js) -> dict[str, typing.Union[str, None]]:
        flow_data = {
            'flow_url': None,
            'ass_param1': 'AgLK2',
            'ass_param2': 'MEuBS5',
            'turnstile_siteKey': None,
            'onload_token': None,
        }

        for i,v in enumerate(js.split('~/')):
            if len(v.split(':')) > 2:
                js2 = v.split('/~')
                for s in js2:
                    if str(round(time.time()))[:5] in s and len(s.split(':')) == 3:
                        flow_data['flow_url'] = s

        for i,v in enumerate(js.split("='")):
            print(v)
            if len(v.split('~')) > 500:
                for code in v.split('~'):
                    print(len(code), code)
                    if len(code) == 65:
                        flow_data['turnstile_siteKey'] = code

                    if len(code) == 50 and 'explicit' in code:
                        flow_data['onload_token'] = code.split('onload=')[1].split('&')[0]

        #for i,v in enumerate(js.split('](setTimeout,')):
        #    print(i, v, '\n')
        #    if len(v.split(':')) > 16 and len(v.split(':')) < 21: #and ('eM' in v and '.md' in v):
        #        print(v)

        #for i,v in enumerate(js.split("='")):
        #    if len(v.split('~')) > 1000:
        #        storaged_c
        return flow_data

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

        - code 4 (turnstile solver):
            cf = CF_Solver(
                'https://nopecha.com/demo/cloudflare',
                siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
            )
            solved = cf.solve_turnstile()

    """

    def __init__(
        self, 
        domain: str, 
        *,
        siteKey: str = None,
        clientRequest: typing.Any = None, 
        userAgent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        jsd_main : str = '/cdn-cgi/challenge-platform/scripts/jsd/main.js',
        jsd_request: str = '/cdn-cgi/challenge-platform/h/g/jsd/r',
        proxy: typing.Union[str, dict] = None
    ):
        self.domain = domain
        self.siteKey = siteKey
        self.client = clientRequest
        self.userAgent = userAgent
        self.jsd_main = jsd_main
        self.jsd_request = jsd_request
        self.proxy_obj = proxy

        if self.client is None:
            self.client = httpx.Client(
                headers={
                    'accept': '*/*',
                    'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
                    'user-agent': self.userAgent,
                    'content-type': 'application/json',
                    'referer': self.domain + '/',
                    'origin': self.domain
                },
                proxy=self._proxy_dict(),
                timeout=10
            )

        self.cf_ray: typing.Optional[str] = None
        self.baseStr = lambda base_dict: json.dumps(base_dict, separators=(',', ':'))
        self.d: typing.Optional[str] = None
        self.b: typing.Optional[str] = None

        super().__init__(
            domain=self.domain,
            clientRequest=self.client, 
            userAgent=self.userAgent,
            jsd_main_url=self.jsd_main
        )

    def _proxy_dict(self):
        if self.proxy_obj is not None:
            if 'https://' in self.proxy_obj:
                return self.proxy
            else:
                return 'https://' + self.proxy_obj

    def solve_flow_ov1(
        self, 
        flow_url,
        siteKeyT,
        encoder_path='interactive_encoder.js', 
        flow_auto=False,
        cf_interactive_auto: types.FunctionType = None,
        managed_data=False,
        **kwargs
    ):
        """
        Turnstile flow_url part: 1713980851:1729499767:J-2EUfnJIDkf89j3D5flgXfV1SSZL6Pi8VXL6ISrhEE
        """

        if self.d is None:
            self.d, self.b, self.cf_ray = parse_cf_params(
                domain=self.domain, 
                siteKey=self.siteKey,
                client=self.client
            )

        #print(self.d)

        cRay = self.d[33].split("'")[1]
        cHash = self.d[34].split("'")[1]
        cH = self.d[35].split("'")[1]
        print(cRay, cHash, cH)

        if not flow_auto:
            if managed_data:
                flow_base = CF_Interactive.cf1_flow_data(self.d)
                base_str = self.baseStr(flow_base)
            else:
                flow_base = CF_Interactive.cf1_flow_data(self.d, kwargs['p1'], kwargs['p2'])
                base_str = self.baseStr(flow_base)
        else:
            flow_base = cf_interactive_auto(self.b, cRay, self.siteKey, kwargs['p1'], kwargs['p2'])
            base_str = self.baseStr(flow_base)

        print(base_str, siteKeyT)

        result = subprocess.run(
            ['node', encoder_path, base_str, siteKeyT],
            capture_output=True,
            text=True
        )
        flow_token = result.stdout.strip()
        print(flow_token)
        sys.exit()

        data = {
            f'v_{cRay}': flow_token
        }
        flow = self.client.post(
            f'{self._domain_parsed}/cdn-cgi/challenge-platform/h/b/flow/ov1/{flow_url}/{cRay}/{cHash}',
            data=data
        )
        print('cf', flow, flow.text)

    def solve_turnstile(self):
        """
        BETA
        """
        flow_data = self.parse_orchestrate_params(js=self.cf_orchestrate_js())
        flow_url = flow_data['flow_url']
        p1, p2 = flow_data['ass_param1'], flow_data['ass_param2']
        _siteKey = flow_data['turnstile_siteKey']
        print(flow_data, flow_url, p1, p2, _siteKey)

        # 1
        self.solve_flow_ov1(
            flow_url=flow_url,
            siteKeyT=_siteKey,
            p1=p1,
            p2=p2
        )
        sys.exit()

        # 2
        flow_data_auto = self.parse_orchestrate_params(js=self.cf_orchestrate_js(True))


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
        'https://nopecha.com/demo/cloudflare',
        siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
        #jsd_main='/cdn-cgi/challenge-platform/h/b/scripts/jsd/62ec4f065604/main.js',
        #jsd_request='/cdn-cgi/challenge-platform/h/b/jsd/r'
    )
    cf.solve_turnstile()
