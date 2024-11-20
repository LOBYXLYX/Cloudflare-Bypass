import time
import sys
import types
import json
import httpx
import execjs
import typing
import random
import uuid
import subprocess
import threading

from dataclasses import dataclass
from wb_base_data import wbBaseData
from interactive_data import CF_Parser, CF_Interactive
from orchestrate_full_reverse import OrchestrateJS, VM_Automation


@dataclass
class CF_MetaData:
    domain: str = None
    clientRequest: typing.Union[typing.Any, httpx.Client] = None
    userAgent: typing.Optional[str] = None

    jsd_main_url: str = None
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

        # search index
        def _func_g_index():
            func_g = r.split("'g'")

            for i,func in enumerate(func_g):
                if len(func) > 1800:
                    return i

        func_g = r.split("'g'")[_func_g_index()].split("},'")[0].split('1.')

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

    def _get_ray_and_chltK(self) -> tuple[str, str]:
        self.clientRequest.headers.update(self.update_sec_header('navegate'))

        r = self.clientRequest.get(self.domain, follow_redirects=True)
        chl_tk = self._domain_parsed + '/'

        if '__cf_chl_rt_tk' in r.text:
            rt_tk = r.text.split('__cf_chl_rt_tk=')[1].split('",')[0]
            chl_tk = f'{self.domain}?__cf_chl_rt_tk={rt_tk}'

        return r.headers['CF-RAY'].split('-')[0], chl_tk

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

    @staticmethod
    def parse_domain(domain):
        return 'https://' + domain.split('/')[2] if len(domain.split('/')) > 3 else domain

    def cf_orchestrate_js(self, auto_mode=False):
        self._domain_parsed = CF_MetaData.parse_domain(self.domain)
        cf_ray, chl_tk_referer = self._get_ray_and_chltK()
        chl_code = None


        interactive_data = OrchestrateJS.get_orchestrate_data()
        key1 = f'~{list(interactive_data.keys())[0]}~'

        self.clientRequest.headers.update({
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'referer': chl_tk_referer,
            **self.update_sec_header('script')
        })
        url = f'{self._domain_parsed}/cdn-cgi/challenge-platform/h/b/orchestrate/chl_page/v1'
        params = {
            'ray': cf_ray,
        }
        if auto_mode:
            params['lang'] = 'auto'
            url = f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/orchestrate/chl_api/v1' 

        def _send_orche_thread() -> None:
            nonlocal chl_code, params, url, key1

            chl = self.clientRequest.get(url, params=params)
            if ('100,g,' in chl.text or '100,e,' in chl.text) and key1 not in chl.text:
                chl_code = chl.text
            else:
                return _send_orche_thread()

        thread = threading.Thread(target=_send_orche_thread)
        thread.start()

        while not chl_code:
            #print('waiting orchestrate javascript code')
            time.sleep(0.1)

        thread.join()
        open('cloudflare-data/cf_code.txt', 'w').write(chl_code)
        return chl_code

    def parse_challenge_auto(self, siteKey) -> tuple[list[str], str]:
        cf_reversed_js = execjs.compile(open('cf_reversed_funcs.js', 'r').read())
        l = cf_reversed_js.call('l')
        ov2_t_url = f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/if/ov2/av0/rcv0/0/{l}/{siteKey}/dark/fbE/normal/auto/'
        self.clientRequest.headers.update(self.update_sec_header('iframe'))

        ca = self.clientRequest.get(ov2_t_url).text
        chl_opt = ca.split('window._cf_chl_opt={')[1].split(':')
        return chl_opt, ov2_t_url

    def challenge_onload(self, flow_data) -> str:
        onload = flow_data['onload_token']
        this_key = flow_data['really_a_key']

        params = {
            'onload': onload,
            'render': 'explicit'
        }
        onload_javascript = self.clientRequest.get(
            f'https://challenges.cloudflare.com/turnstile/v0/b/{this_key}/api.js',
            parsms=params
        )

        # modify javascript code
        r = onload_javascript.replace('function fr(){var e=At();e||m("Could not find Turnstile script tag, some features may not be available",43777);var r=e.src,n={loadedAsync:!1,params:new URLSearchParams,src:r};(e.async||e.defer)&&(n.loadedAsync=!0);var o=r.split("?");return o.length>1&&(n.params=new URLSearchParams(o[1])),n}', '')
        r = r.replace('throw new dr(n,r)', '')
        return r

    def generate_blob_urls(self, c=4) -> dict[str, list[str]]:
        url1 = f'blob:https://challenges.cloudflare.com/'
        url2 = f'blob:{CF_MetaData.parse_domain(self.domain)}/'

        blobs = {
            'challenges': [],
            'this_website': []
        }
        for i in range(c):
            if i % 2 == 0:
                blobs['challenges'].append(url1 + uuid.uuid4())
            else:
                blobs['this_website'].append(url2 + uuid.uuid4())
        return blobs

    def update_sec_header(self, _type='cors') -> dict:
        sec_headers = {
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin'
        }

        if _type == 'script':
            sec_headers['sec-fetch-dest'] = 'script'
            sec_headers['sec-fetch-mode'] = 'no-cors'
            sec_headers['sec-fetch-site'] = 'same-origin'
        elif _type == 'navegate':
            sec_headers['sec-fetch-dest'] = 'document'
            sec_headers['sec-fetch-mode'] = 'navegate'
            sec_headers['sec-fetch-site'] = 'none'
        elif _type == 'iframe':
            sec_headers['sec-fetch-dest'] = 'iframe'
            sec_headers['sec-fetch-mode'] = 'navegate'
            sec_headers['sec-fetch-site'] = 'cross-site'
        return sec_headers

class CF_TurnstileBase(CF_MetaData):
    def __init__(
        self,
        *,
        domain: str,
        OtherSiteKey: str,
        clientRequest: typing.Union[typing.Any, httpx.Client],
        userAgent: str = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.46 Mobile/15E148 Safari/604.1',
    ):
        self.domain = domain
        self.userAgent = userAgent
        self.client = clientRequest
        self.OtherSiteKey = OtherSiteKey

        self.cRay: typing.Optional[str] = None

        super().__init__(
            domain=self.domain,
            userAgent=self.userAgent,
            clientRequest=self.client,
            jsd_main_url='/cdn-cgi/challenge-platform/scripts/jsd/main.js'
        )

        self.baseStr = lambda base_dict: json.dumps(base_dict, separators=(',', ':'))
        self.d = None
        self.b = None
        self.cRay = None
        self.main_domain = CF_MetaData.parse_domain(self.domain)
        self.vm_automation = VM_Automation(self.domain, self.userAgent)

        if not (self.d or self.b):
            self.init_cf_params()

        self.d_find_value = lambda index: self.d[index].split("'")[1]
        self.b_find_value = lambda index: self.b[index].split("'")[1]

    def parse_cf_orchestrate(self, auto=False) -> dict[str, typing.Union[str, None]]:
        data = self.parse_orchestrate_params(js=self.cf_orchestrate_js(auto))
        return data

    def init_cf_params(self):
        self.d, self.b, self.cf_ray = CF_Parser.cf_params(
            domain=self.domain,
            siteKey=self.OtherSiteKey,
            client=self.client
        )

    def build_flow_ov1(self, is_flow_auto: bool, chl: list = None) -> tuple[str, str]:
        if not is_flow_auto:
            return self.cRay + '/' + self.d_find_value(5), self.d_find_value(5)
        else:
            return self.cRay + '/' + chl[16].split("'")[1], chl[16].split("'")[1]

    def solve_flow_ov1(
        self,
        flow_url: str, 
        siteKey: str,
        encoder_path: str,
        flow_auto: bool,
        cf_interactive: dict[str, typing.Any],
        encrypter_floats: str,
        chl_opt: list[str] = None
    ):
        base_interactive = self.baseStr(cf_interactive)
        result = subprocess.run(
            ['node', encoder_path, base_interactive, siteKey, encrypter_floats],
            capture_output=True,
            text=True
        )
        flow_token = result.stdout.strip()

        if self.cRay is None:
            self.cRay = self.d_find_value(4)

        flow_url_part, cf_challenge_value = self.build_flow_ov1(flow_auto, chl_opt)
        complet_flow_url = f'{self.main_domain}/cdn-cgi/challenge-platform/h/b/flow/ov1/{flow_url}/' + flow_url_part

        self.vm_automation.send_ov1_request(
            flowUrl=complet_flow_url, 
            flowToken=flow_token,
            cfChallenge=cf_challenge_value,
            cfRay=self.cRay
        )
                
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

        - code 5 (set headers):
            cf = CF_Solver(
                'https://www.example.com',
                headers={
                    'authorization': some_token,
                    'x-client-id': 123456
                }
            )
    """

    def __init__(
        self, 
        domain: str, 
        *,
        siteKey: str = None,
        clientRequest: typing.Any = None, 
        userAgent: str = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.46 Mobile/15E148 Safari/604.1',
        jsd_main : str = '/cdn-cgi/challenge-platform/scripts/jsd/main.js',
        jsd_request: str = '/cdn-cgi/challenge-platform/h/g/jsd/r',
        proxy: typing.Union[str, dict] = None,
        web_cookies: bool = True,
        headers: dict[str, typing.Any] = {}
    ):
        self.domain = domain
        self.siteKey = siteKey
        self.client = clientRequest
        self.userAgent = userAgent
        self.jsd_main = jsd_main
        self.jsd_request = jsd_request
        self.proxy_obj = proxy
        self.web_cookies = web_cookies
        self.headers = headers

        if self.client is None:
            self.client = httpx.Client(
                headers={
                    'accept': '*/*',
                    'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
                    'user-agent': self.userAgent,
                    'content-type': 'application/json',
                    'referer': self.domain + '/',
                    'origin': CF_MetaData.parse_domain(self.domain),
                    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="129", "Google Chrome";v="129"',
                    'sec-ch-ua-mobile': '?1',
                    'sec-ch-ua-platform': '"iOS"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'none',
                    **self.headers
                },
                proxy=self._proxy_dict(),
                timeout=10
            )

        self.cf_ray: typing.Optional[str] = None

        if self.web_cookies:
            self._website_cf_cookies()

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

    def _website_cf_cookies(self):
        cf_cookies_types = (
            '__cf_bm',
            '__cfruid',
            '_cfuvid',
        )

        site = self.client.get(self.domain)
        self.client.cookies.clear()

        for cookie_name, value in site.cookies.items():
            if cookie_name in cf_cookies_types:
                self.client.cookies.set(
                    name=cookie_name, 
                    value=value, 
                    domain='.' + self.domain.replace('https://', '')
                )

        if not len(self.client.cookies) > 0: # Try another method
            if 'window.__CF$cv$params=' in site.text and self.jsd_main in site.text:
                # get __cf_bm
                cookie = self.client.get(self.domain + self.jsd_main).cookies
                self.client.cookies = cookie


    def solve_turnstile(self):
        cf_turnstile = CF_TurnstileBase(
            domain=self.domain,
            OtherSiteKey=self.siteKey,
            clientRequest=self.client,
            userAgent=self.userAgent
        )

        def _get_orchestrate_data(auto_mode=False) -> tuple[object, str, str]:
            js = self.cf_orchestrate_js(auto_mode)

            oj = OrchestrateJS(js, auto_mode=auto_mode)
            oj.parse_params()
            enc_floats = oj.get_encrypter_floats()

            return oj, js, enc_floats

        oj, cf_js, enc_f = _get_orchestrate_data()
        cf_int1 = CF_Interactive(cf_js, cf_turnstile.d, False)

        cf_turnstile.solve_flow_ov1(
            flow_url=oj.flow_data['flow_url'],
            siteKey=oj.flow_data['turnstile_siteKey'],
            encoder_path='interactive_encoder.js',
            flow_auto=False,
            cf_interactive=cf_int1.cf1_flow_data(),
            encrypter_floats=enc_f
        )
        print('\n')
        # stage 2~39
        oj2, cf_js2, enc_f2 = _get_orchestrate_data(True)
        cf_int2 = CF_Interactive(cf_js2, cf_turnstile.b, True)
        chl_opt, ov1_url = self.parse_challenge_auto(self.siteKey)

        cf_turnstile.solve_flow_ov1(
            flow_url=oj2.flow_data['flow_url'],
            siteKey=oj2.flow_data['turnstile_siteKey'],
            encoder_path='chl_api_encoder.js',
            flow_auto=True,
            cf_interactive=cf_int2.cf2_flow_data(self.domain, CF_MetaData.parse_domain(self.domain)),
            encrypter_floats=enc_f2,
            chl_opt=chl_opt
        )

    def cookie(self): 
        wb, s_param, self.cf_ray = self.cf_cookie_parse()
        payload = {
            'wb': wb,
            's': s_param
        }

        self.client.headers.update(self.update_sec_header())

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
