import time
import sys
import types
import json
import execjs
import typing
import random
import uuid
import subprocess
import threading
import tls_client

from dataclasses import dataclass
from wb_base_data import wbBaseData
from interactive_data import CF_Parser, CF_Interactive
from reverse_decrypter import analyze_response
from orchestrate_full_reverse import (
    OrchestrateJS, 
    VM_Automation,  
    ReversedObjects
)

@dataclass
class CF_MetaData:
    domain: str = None
    clientRequest: typing.Any = None
    userAgent: typing.Optional[str] = None

    jsd_main_url: str = None
    _domain_parsed: typing.Optional[str] = None
    _headers_device_identifier = {
        'sec-ch-ua-arch': '"x86_64"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"120.0.0.0"',
        'sec-ch-ua-full-version-list': '"Chromium";v="120.0.0.0", "Not_A Brand";v="24.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.2.1"'
    }

    def clearance_analyzer(self) -> typing.Tuple[typing.Optional[str], str, ...]:
        r = self.clientRequest.get(self.domain + self.jsd_main_url)

        if r.status_code == 302 and 'Location' in r.headers: # pls add auto_redirection to tls_client libraru
            r = self.clientRequest.get(self.domain + r.headers['Location'])

        html_site = r.text

        s_param = None
        cf_ray = r.headers['Cf-Ray'].split('-')[0]

        for i,v in enumerate(html_site.split(',/')):
            if v.startswith('jsd/r/'):
                s_param = v.split('/,')[0]
                break

        v_tps = [
            'a', 'b', 'z', 'f', 'e', 'm', 'n', 
            'p', 'g', 'h', 'j', 'k', 'l', 'y',
            'Z', 'x', 'v', 'q', 'd', 's', 't'
        ]

        for vtp in v_tps:
            for i,v in enumerate(html_site.split(f'function {vtp}(')):
                vb = v[:1300]

                if vb.count(',') > 60 and 'return ' in vb[:15] and (
                    '_cf_chl_opt' in vb or '/jsd/r' in vb or '/cdn-cgi' in vb
                ) and v[2:3] == ')':
                    variab = v[:2]
                    break

        spli1 = html_site.split(f"{variab}='")[1].split(',')

        for i, v in enumerate(spli1):
            if len(v) == 65:
                siteKey = v
                break

        def _encrypter(data, siteKey):
            func_g = None

            def _parseInt_values(fv) -> str:
                spli1 = html_site.split(f'({fv}=')[1].split('.push(')[0].split('===')[0]
        
                test = spli1.replace('\n', '').replace(' ', '')
                if '),' in test[(len(test) - 5):len(test)]:
                    spli2 = (spli1.split('),')[0] + '),')

                elif ',' in test[(len(test) - 5):len(test)]:
                    spli2 = (spli1.split(',')[0] + ',')
            
                spli2 = spli2.replace('\n', '').strip().replace(' ', '')
        
                variable = spli2.split('parseInt(')[1][:1]
                _parseInt = spli2.replace(variable, 'gE')
                return _parseInt

            for i,v in enumerate(html_site.split(f"'g':function(")):
                if len(v[:35].split(',')) > 10 and 'Object[' in v:
                    func_g = 'function g(' + v.split(",'j':function")[0]

                    p = 2
                    if v[:115].split('{if(')[1][1:2] == '=':
                        p = 1
                    b_v = v[:115].split('{if(')[1][:p]
                    p = 2

                    if v[:115].split('{if(' + f'{b_v}=')[1][1:2] == '=':
                        p = 1
                    o_v = v[:115].split('{if(' + f'{b_v}=')[1][:p]

                    if ',' in o_v:
                        o_v = o_v.split(',')[0]

                    func_g = func_g.replace(f'{b_v}={o_v},', f'{b_v} = (number) => b(number),')
                    break
    
            for i,v in enumerate(html_site.split('parseInt(')):
                if '}}(' in v[:400]:
                    variaba = v.split('}(')[1][:2]
                    obf_number = int(v.split('}(' + variaba)[1].split('),')[0].strip())
                if 'window._' in v[:15] and i == 0:
                    fv = v.split('try{if(')[1][:1]

            parseInt_gen = _parseInt_values(fv)

            js = html_site.split(f"{variab}='")[1].split("'.split(")[0]
            f_less = int(html_site.split('f=f-')[1].split(',')[0])

            result = VM_Automation.encrypt_flow_data(
                data, 
                siteKey, 
                func_g, 
                b_v, 
                '',
                split_type=',',
                f_less=f_less,
                obf_code=js,
                obf_number=obf_number,
                parseint_gen=parseInt_gen,
                parentesis=''
            )
            return result

        return siteKey, s_param, cf_ray, _encrypter

    def _get_ray_and_chltK(self) -> tuple[str, str]:
        r = self.clientRequest.get(self.domain)
        chl_tk = self._domain_parsed + '/'

        if '__cf_chl_rt_tk' in r.text:
            rt_tk = r.text.split('__cf_chl_rt_tk=')[1].split('"')[0]
            chl_tk = f'{self.domain}?__cf_chl_rt_tk={rt_tk}'
            ReversedObjects.cf_chl_opt['_rttk'] = rt_tk

        return r.headers['Cf-Ray'].split('-')[0], chl_tk

    def cf_cookie_parse(self) -> tuple[str, typing.Optional[str], str]:
        base_data = wbBaseData(
            domain=self.domain.replace('https://', ''),
            useragent=self.userAgent
        )
        base_str = json.dumps(base_data, separators=(',', ':'))
        siteKey, s, cf_ray, encrypter = self.clearance_analyzer()

        wb = encrypter(base_str, siteKey)
        return wb, s, cf_ray

    @staticmethod
    def parse_domain(domain):
        return 'https://' + domain.split('/')[2] if len(domain.split('/')) > 3 else domain

    def cf_orchestrate_js(self, auto_mode=False, cf_ray=None, ov1_url=None):
        self._domain_parsed = CF_MetaData.parse_domain(self.domain)
        if cf_ray is None:
            cf_ray, chl_tk_referer = self._get_ray_and_chltK()
        else:
            chl_tk_referer = ov1_url
        chl_code = None

        interactive_data = OrchestrateJS.get_orchestrate_data()
        key1 = f'~{list(interactive_data.keys())[0]}~'

        self.clientRequest.headers.update({
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'referer': chl_tk_referer,
        })
        url = f'{self._domain_parsed}/cdn-cgi/challenge-platform/h/g/orchestrate/chl_page/v1'
        params = {
            'ray': cf_ray,
        }
        if auto_mode:
            params['lang'] = 'auto'
            url = f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/orchestrate/chl_api/v1' 

        def _send_orche_thread() -> None:
            nonlocal chl_code, params, url, key1

            chl = self.clientRequest.get(url, params=params)
            if ',100,' in chl.text and key1 not in chl.text:
                chl_code = chl.text
            else:
                return _send_orche_thread()

        #print('cloudflare javascript URL:', url, cf_ray)

        thread = threading.Thread(target=_send_orche_thread)
        thread.start()

        while not chl_code:
            #print('waiting orchestrate javascript code')
            time.sleep(0.1)

        thread.join()
        open('cloudflare-data/cf_code.txt', 'w').write(chl_code)
        return chl_code

    def parse_challenge_auto(self, siteKey) -> tuple[list[str], str, list[str], str, str]:
        cf_reversed_js = execjs.compile(open('cf_reversed_funcs.js', 'r').read())
        l = cf_reversed_js.call('l')
        ov2_t_url = f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/turnstile/if/ov2/av0/rcv/{l}/{siteKey}/dark/fbE/new/normal/auto/'

        ca = self.clientRequest.get(ov2_t_url).text
        chl_opt = ca.split('window._cf_chl_opt={')[1].split(':')

        rep = self.clientRequest.get(self.domain)
        d = rep.text.split(':')
        ray = rep.headers['Cf-Ray'].split('-')[0]

        return chl_opt, ov2_t_url, d[28:len(d)], chl_opt[15].split("'")[1], ca, rep.text

    def challenge_onload(self, flow_data, callback=False) -> str:
        onload = flow_data['onload_token']
        this_key = flow_data['really_a_key']

        params = {
            'onload': onload,
            'render': 'explicit'
        }
        if callback:
            params['render'] = 'onloadTurnstileCallback'

        onload_javascript = self.clientRequest.get(
            f'https://challenges.cloudflare.com/turnstile/v0/g/{this_key}/api.js',
            params=params
        ).text

        # modify javascript code
        r = onload_javascript.replace('function fr(){var e=At();e||m("Could not find Turnstile script tag, some features may not be available",43777);var r=e.src,n={loadedAsync:!1,params:new URLSearchParams,src:r};(e.async||e.defer)&&(n.loadedAsync=!0);var o=r.split("?");return o.length>1&&(n.params=new URLSearchParams(o[1])),n}', '')
        r = r.replace('throw new dr(n,r)', '').replace('fr()', 'null')
        return r

class CF_TurnstileBase(CF_MetaData):
    def __init__(
        self,
        *,
        domain: str,
        OtherSiteKey: str,
        clientRequest: typing.Any,
        userAgent: str = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.46 Mobile/15E148 Safari/604.1',
        turnstileCallback: bool = False
    ):
        self.domain = domain
        self.userAgent = userAgent
        self.client = clientRequest
        self.OtherSiteKey = OtherSiteKey
        self.callback = turnstileCallback

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
        self.turnstile_html = None
        self.site_html = None
        self.main_domain = CF_MetaData.parse_domain(self.domain)

        if not (self.d or self.b):
            self.init_cf_params()

        self.vm_automation = VM_Automation(
            domain=self.domain, 
            userAgent=self.userAgent,
            cf_html=True,
            html_code=self.site_html
        )
        self.utility = execjs.compile(open('_reverse_utility.js', 'r').read())
        self.cloudflare_js = None

        self.d_find_value = lambda index: self.d[index].split("'")[1]
        self.b_find_value = lambda index: self.b[index].split("'")[1]

    def init_cf_params(self):
        self.b, self.ov1_url, self.d, self.cf_ray, self.turnstile_html, self.site_html = self.parse_challenge_auto(self.OtherSiteKey)
        print(self.b, self.d)

    def build_flow_ov1(self, is_flow_auto: bool, chl: list = None) -> tuple[str, str]:
        if not is_flow_auto:
            return self.cRay + '/' + self.d_find_value(5), self.d_find_value(5)
        else:
            return self.cRay + '/' + chl[16].split("'")[1], chl[16].split("'")[1]

    def post_message(self, flow_data, _data: dict[str, typing.Any]):
        if not ReversedObjects.initialized_onload:
            onload_javascript = self.challenge_onload(flow_data, self.callback)
            ReversedObjects.initialized_onload = True
            ReversedObjects.onload_challenge = onload_javascript
        else:
            onload_javascript = ReversedObjects.onload_challenge

        self.vm_automation.onload_postMessage(onload_javascript, _data)

    def simple_request(self, url, new_headers):
        self.client.headers.update(new_headers)
        return self.clientRequest.get(url).text

    def send_ov1_request(
        self,
        flowUrl: str,
        flowToken: str,
        cfChallenge: str,
        referrer: str,
        decrypter: types.FunctionType
    ):
        self.client.headers.update({
            'cf-challenge': cfChallenge,
            'cf-chl-retryattempt': '0',
            'save-data': 'on',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': referrer
        })
        print('cloudflare challenge URL:\033[36m', flowUrl, '\033[0m')
        print('request payload:', f'v_{self.cRay}={flowToken[:100]}....')

        response = self.client.post(flowUrl, data={f'v_{self.cRay}': flowToken}).text

        print('cloudflare response:\033[32m', response[:100]+'....', '\033[0m')

        if '"err"' in response:
            raise TypeError(f'Cloudflare Challenge Failed {response}')

        window_decrypted = decrypter(response, self.cRay)
        print(window_decrypted)
        return window_decrypted

    def solve_flow_ov1(
        self,
        flow_url: str, 
        siteKey: str,
        flow_auto: bool,
        cf_interactive: dict[str, typing.Any],
        encrypter: types.FunctionType,
        chl_opt: list[str] = None,
        notdecrypter: types.FunctionType = None,
        evaluate_window: bool = True,
        **kwargs
    ) -> tuple[typing.Optional[dict], typing.Optional[dict]]:
        base_interactive = self.utility.call('parseUndefined', self.baseStr(cf_interactive))
        print(base_interactive)
        flow_token = encrypter(base_interactive, siteKey)

        if flow_auto:
            self.cRay = chl_opt[15].split("'")[1]
            ReversedObjects.cf_chl_opt['chlApicData'] = self.cRay
        else:
            self.cRay = self.d_find_value(4)

        flow_url_part, cf_challenge_value = self.build_flow_ov1(flow_auto, chl_opt)
        if flow_auto:
            complet_flow_url = f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/flow/ov1/{flow_url}/' + flow_url_part
            ReversedObjects.challenge_cloudflare = flow_url
            referrer = self.ov1_url
        else:
            complet_flow_url = f'{self.main_domain}/cdn-cgi/challenge-platform/h/g/flow/ov1/{flow_url}/' + flow_url_part
            ReversedObjects.challenge_website = flow_url
            referrer = self.domain

        if 'decrypter_response' in kwargs:
            decrypter = kwargs['decrypter_response']

        _window_decrypted = self.send_ov1_request(
            flowUrl=complet_flow_url, 
            flowToken=flow_token,
            cfChallenge=cf_challenge_value,
            referrer=referrer,
            decrypter=decrypter
        )
        if evaluate_window:
            if _window_decrypted.startswith('window._'):
                eval_result = self.vm_automation.evaluate(
                    code=_window_decrypted, 
                    decryptedChl=base_interactive, 
                    flow_auto=flow_auto,
                    previous_data=base_interactive
                )
            else:
                print(_window_decrypted[:300])
                decrypted = notdecrypter(
                    vm=self.vm_automation, 
                    response=_window_decrypted, 
                    base_interactive=base_interactive,
                    parsed_functions=analyze_response(self.cloudflare_js)
                )
        else:
            eval_result = _window_decrypted
        return OrchestrateJS.extract_decrypted_data(_window_decrypted, flow_auto), eval_result

    def solve_cap_interaction(
        self, 
        interaction_code: str, 
        cf_interactive: dict[str, typing.Any]
    ):
        base_interactive = self.utility.call('parseUndefined', self.baseStr(cf_interactive))
        result = self.vm_automation.evaluate_captcha(
            code=interaction_code,
            decryptedChl=base_interactive
        )
        return result
                
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
        userAgent: str = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.0.0 Mobile/15E148 Safari/604.1',
        jsd_main : str = '/cdn-cgi/challenge-platform/scripts/jsd/main.js',
        jsd_request: str = '/cdn-cgi/challenge-platform/h/b',
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
            self._algorithms = [
                'PKCS1WithSHA256',
                'PKCS1WithSHA384',
                'PKCS1WithSHA512'
                'PSSWithSHA256'
                'PSSWithSHA384'
                'PSSWithSHA512'
                'ECDSAWithP256AndSHA256'
                'ECDSAWithP384AndSHA384'
                'ECDSAWithP521AndSHA512'
                'PKCS1WithSHA1'
                'ECDSAWithSHA1'
            ]
            self.client = tls_client.Session(
                client_identifier='chrome_120',
                random_tls_extension_order=True,
                supported_versions=[
                    'GREASE', 
                    '1.3', 
                    '1.2',
                    'P256',
                    'P384'
                ],
                key_share_curves=[
                    'GREASE', 
                    'X25519',
                    'secp256r1',
                    'secp384r1',
                    'Unknown curve 0x11EC'
                ],
                h2_settings={
                    'HEADER_TABLE_SIZE': 65536,
                    'MAX_CONCURRENT_STREAMS': 1000,
                    'INITIAL_WINDOW_SIZE': 6291456,
                    'MAX_HEADER_LIST_SIZE': 262144
                },
                h2_settings_order=[
                    'HEADER_TABLE_SIZE',
                    'MAX_CONCURRENT_STREAMS',
                    'INITIAL_WINDOW_SIZE',
                    'MAX_HEADER_LIST_SIZE'
                ],
                supported_delegated_credentials_algorithms=self._algorithms,
                supported_signature_algorithms=self._algorithms,
                cert_compression_algo='brotli',
                connection_flow=random.randint(48, 64) << 18,
                ja3_string='772,4865-4866-4867-49195-49199-49196-49200-52393-52392-49171-49172-156-157-47-53,27-13-10-23-5-16-35-65281-45-18-65037-43-17513-51-11-0,4588-29-23-24,0', # automatized ja$
                pseudo_header_order=[
                    ':authority',
                    ':scheme',
                    ':path'
                ],
                header_order=[
                    'accept'
                    'accept-language',
                    'user-agent',
                    'content-type',
                    'referer',
                    'origin'
                ]
            )
            self.client.proxies = self._proxy_dict()
            self.client.headers = {
                'accept': '*/*',
                'accept-language': 'es-US,es-419;q=0.9,es;q=0.8',
                'user-agent': self.userAgent,
                'content-type': 'application/json',
                'referer': self.domain + '/',
                'origin': CF_MetaData.parse_domain(self.domain),
                'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'sec-ch-ua-mobile': '??',
                'sec-ch-ua-platform': '"iOS"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                **self.headers
                #**self._headers_device_identifier
            }

        self.cf_ray: typing.Optional[str] = None

        if self.web_cookies:
            self._website_cf_cookies()

        ReversedObjects.cf_chl_opt['chlApiUrl'] = self.domain

        super().__init__(
            domain=self.domain,
            clientRequest=self.client, 
            userAgent=self.userAgent,
            jsd_main_url=self.jsd_main
        )

    def _proxy_dict(self):
        if self.proxy_obj is not None:
            if 'https://' in self.proxy_obj:
                return self.proxy_obj
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
        def _get_orchestrate_data(auto_mode=False, *args) -> tuple[object, str, str]:
            js = self.cf_orchestrate_js(auto_mode, *args)

            oj = OrchestrateJS(js, auto_mode=auto_mode)
            oj.parse_params()
            enc_floats = oj.get_encrypter_floats()

            if oj.flow_data['flow_url'] is None or oj.flow_data['turnstile_siteKey'] is None:
                raise ValueError('Failed to analyze Flow URL/Turnstile siteKey', oj.flow_data)

            return oj, js, enc_floats

        print('TURNSTILE SOLVER DOES NOT WORK ANYMORE, BECAUSE CLOUDFLARE HAS PATCHED IT')

        oj, cf_js, enc_f = _get_orchestrate_data()
        cf_turnstile.cloudflare_js = cf_js
        cf_int1 = CF_Interactive(cf_js, cf_turnstile.d, False)

        result, _eval = cf_turnstile.solve_flow_ov1(
            flow_url=oj.flow_data['flow_url'],
            siteKey=oj.flow_data['turnstile_siteKey'],
            flow_auto=False,
            cf_interactive=cf_int1.cf1_flow_data(),
            encrypter=oj.encrypter_array,
            decrypter_response=oj.decrypter_response,
            notdecrypter=oj.execute_decrypter
        )
        #print(result)
        print('\n')
        # stage 2~6
        oj2, cf_js2, enc_f2 = _get_orchestrate_data(True, cf_turnstile.cf_ray, cf_turnstile.ov1_url)
        cf_turnstile.cloudflare_js = cf_js2
        cf_int2 = CF_Interactive(cf_js2, cf_turnstile.b, True)

        cf_turnstile.post_message(oj.flow_data, {
            'source': 'cloudflare-challenge',
            'widgetId': cf_int2.find_value(9),
            'event': 'requestExtraParams'
        })

        challenge_result, _eval = cf_turnstile.solve_flow_ov1(
            flow_url=oj2.flow_data['flow_url'],
            siteKey=oj2.flow_data['turnstile_siteKey'],
            flow_auto=True,
            cf_interactive=cf_int2.cf2_flow_data(
                self.domain, 
                CF_MetaData.parse_domain(self.domain),
                oj.flow_data['really_a_key'],
                oj.flow_data['onload_token'],
                result['flow2_token'],
                cf_turnstile.cRay
            ),
            encrypter=oj2.encrypter_array,
            chl_opt=cf_turnstile.b,
            decrypter_response=oj2.decrypter_response,
            notdecrypter=oj.execute_decrypter
        )
        #print('lLa', _eval)

        # send clouddlare pat!
        pat = challenge_result['challenge_pat']

        response = cf_turnstile.simple_request(
            f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/{pat}',
            new_headers={
                'referer': cf_turnstile.ov1_url
            }
        )
        
        if not 'J' in response and len(response) > 10:
            print(response)
            sys.exit()
        print('cloudflare pat:', pat[:70], 'got status_code 401')

        # stage 4~6 (It was too difficult)

        challenge_result2, captcha_interaction = cf_turnstile.solve_flow_ov1(
            flow_url=oj2.flow_data['flow_url'],
            siteKey=oj2.flow_data['turnstile_siteKey'],
            flow_auto=True,
            cf_interactive=_eval,
            encrypter=oj2.encrypter_array,
            chl_opt=cf_turnstile.b,
            decrypter_response=oj2.decrypter_response,
            evaluate_window=False
        )
        inter_result = cf_turnstile.solve_cap_interaction(
            interaction_code=captcha_interaction,
            cf_interactive=_eval
        )
        #print('jsjsjjsaja', inter_result)

        cf_turnstile.post_message(oj.flow_data, {
            'source': 'cloudflare-challenge',
            'widgetId': cf_int2.find_value(9),
            'event': 'interactiveEnd'
        })

        challenge_result3, _eval3 = cf_turnstile.solve_flow_ov1(
            flow_url=oj2.flow_data['flow_url'],
            siteKey=oj2.flow_data['turnstile_siteKey'],
            flow_auto=True,
            cf_interactive=inter_result,
            encrypter=oj2.encrypter_array,
            chl_opt=cf_turnstile.b,
            decrypter_response=oj2.decrypter_response,
            evaluate_window=False
        )
        #print(_eval3)
            
        
    def invisible_challenge(self):
        cf_turnstile = CF_TurnstileBase(
            domain=self.domain,
            OtherSiteKey=self.siteKey,
            clientRequest=self.client,
            userAgent=self.userAgent,
            turnstileCallback=True
        )
        def _get_orchestrate_data(*args):
            js_auto = self.cf_orchestrate_js(True, *args)
            js = self.cf_orchestrate_js(False, *args)

            oj = OrchestrateJS(js_auto, auto_mode=True)
            oj.parse_params()

            oj2 = OrchestrateJS(js, auto_mode=False)
            oj2.parse_params()

            return oj, oj2, js_auto

        oj, oj2, cf_js  = _get_orchestrate_data()
        cf_int1 = CF_Interactive(cf_js, cf_turnstile.b, True)

        result, _eval = cf_turnstile.solve_flow_ov1(
            flow_url=oj.flow_data['flow_url'],
            siteKey=oj.flow_data['turnstile_siteKey'],
            flow_auto=True,
            cf_interactive=cf_int1.cf4_flow_data(
                self.domain,
                CF_MetaData.parse_domain(self.domain),
                oj2.flow_data['really_a_key'],
                oj2.flow_data['onload_token'],
                cf_turnstile.cRay
            ),
            encrypter=oj.encrypter_array,
            chl_opt=cf_turnstile.b,
            notdecrypter=oj.execute_decrypter
        )


    def cookie(self): 
        wb, s_param, self.cf_ray = self.cf_cookie_parse()

        jsd = self.client.post(
            f'{self.domain}{self.jsd_request}/{s_param}/{self.cf_ray}',
            data=wb
        )
        return jsd.cookies['cf_clearance']

if __name__ == '__main__':
    cf = CF_Solver(
        'https://nopecha.com/demo/cloudflare',
        siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
    )
    print('Solving Turnstile....')
    cf.solve_turnstile()
