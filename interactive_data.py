import httpx
import typing
import random
import secrets
import base64
import execjs
import uuid
import time

from dataclasses import dataclass
from orchestrate_full_reverse import OrchestrateJS, ReversedObjects
#from aqua import CF_Solver
from wb_base_data import wbBaseData
from Crypto.Random import get_random_bytes


TEST_SITEKEY = '0x4AAAAAAAAjq6WYeRDKmebM'
reversed_funcs = execjs.compile(open('cf_reversed_funcs.js', 'r').read())

class CF_Widget:
    renderEndTime = None
    renderStartTime = None

    initStartTime = None
    paramsStartTime = None

    def timestamp():
        return reversed_funcs.call('W')

class CF_Parser:
    def cf_params(domain, siteKey, client=httpx.Client()) -> tuple[list[str], list[str], str]:
        rep = client.get(domain)
        d = rep.text.split(':')
        ray = rep.headers['CF-RAY'].split('-')[0]
    
        rep2 = client.get(f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/turnstile/if/ov2/av0/rcv0/0/auvka/{siteKey}/dark/fbE/normal/auto/')
        b = rep2.text.split(': ')
        return d[28:len(d)], b[1:len(b)], ray

class FinalChlParams:
    _1 = {
        '01': 'wbBaseData_values',
        '02': random.randint(1000, 50000),
        '03': 'b64_string', # b64,
        '04': '',
        '05': 3,
        '06': {'_06': False},
        '07': 'yes',
        '08': ()
    }
    _2 = {
        '01': random.randint(100, 200),
        '02': 'b64_string', #b64
        '03': '',
        '04': 3,
        '05': 'binascii',
        '06': 'yes',
        '07': 'undefined'
    }
    _3 = {
        '01': [],
        '02': 2,
        '03': 'b64_string', #b64
        '04': '',
        '05': 3,
        '06': 'yes',
        '07': ['lang', 'dir'],
        '08': False,
        '09': '2',
        '10': ()
    }
    _4 = {
        '01': random.randint(10, 200),
        '02': 'b64_string', #b4,
        '03': '',
        '04': 3,
        '05': 'yes',
        '06': 'binascii',
        '07': 'undefined'
    }
    _5 = {
        '01': 'htm_la_di>hea>tit>-tmet_ht_co>met_ht_co>met_na_co>met_na_co>sty>-tmet_ht_co>scr_sr>sty>-tscr_sr_as_de_cr>bod_cl>div_cl_ro>div_cl>h1_cl>',
        '02': 0,
        '03': 'https://nopecha.com/demo/cloudflare',
        '04': 'b64_string', # b64
        '05': '',
        '06': 3,
        '07': True,
        '08': 2,
        '09': (2**31) + random.randint(100000000, 400000000),
        '10': 'yes',
        '11': 4,
        '12': 5,
        '13': '/div[1]/div[1]/div[1]/div[1]/div[1]',
        '14': 43
    }
    _6 = {
        '01': 'XtyOsXtyOsrootrootroot',
        '02': random.randint(10, 200),
        '03': 'b64_string', #b4
        '04': '',
        '05': 3,
        '06': 'random',
        '07': ()
    }
    _7 = {
        '01': 'yes',
        '02': 0,
        '03': 'b64_string', #b64,
        '04': '',
        '05': 3,
        '06': 'yes',
        '07': ()
    }
    _8 = {
        '01': 'status_401',
        '02': random.randint(500, 2000),
        '03': 'b64_string', #b64,
        '04': '',
        '05': 3,
        '06': 'yes',
        '07': 'undefined'
    }
    _9 = {
        '01': 5,
        '02': False,
        '03': 0.8,
        '04': 'b64_string',#b64
        '05': False,
        '06': '',
        '07': 3,
        '08': -1,
        '09': False,
        '10': random.randint(1000, 20000),
        '11': 'yes',
        '12': False,
        '13': True,
        '14': True,
        '15': 'undefined'
    }
    _10 = {
        '01': random.randint(10, 200),
        '02': 'b64_string',#b64
        '03': '',
        '04': 3,
        '05': 'yes',
        '06': 'unknown_token',
        '07': 'undefined'
    }
    _11 = {
        '01': [
            {"t": "n", "i": "navigate"},
            {"t": "v", "s": 0, "d": 0},
            {"t": "lf"},
            {"t": "r", "dlt": random.uniform(100, 50000), "i": "link", "n": "https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/cmg/1", "nh": "h3","ts": 361, "bs": 61},
            {"t": "r", "dlt": random.uniform(100, 50000), "i": "script", "n": "https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/orchestrate/chl_api/v1?ray=8de6c4cf6d6ca5f0&lang=auto", "nh": "h3", "ts": random.randint(1000, 60000), "bs": random.randint(1000, 60000)},
            {"t": "lf"},
            {"t": "lf"},
            {"t": "p","i": "first-paint"},
            {"t": "p", "i": "first-contentful-paint"},
            {"t": "lf"},
            {"t": "v", "s": random.uniform(100, 50000),"d": 0},
            {"t": "v","s": random.uniform(100, 50000), "d": 0},
            {
                "t": "r",
                "dlt": random.uniform(100, 50000),
                "i": "xmlhttprequest",
                "n": "https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/flow/ov1/1037485612:1730910539:AsDcWZz6St2tT52FfsrQ3kdbv-1pL7gMo2fXlxCqkzU/8de6c4cf6d6ca5f0/iAzHWl20I.x6jIqoYkTFXCKjn6fezHfVe1J29_77iYo-1730913779-1.1.1.1-0kcX6bLhDgC2mKF3tpYMwu.PY3cEaoR5MgU6vETNpQTGRTnJZK9NvygTnD.if3ye",
                "nh": "h3",
                "ts": random.randint(1000, 60000),
                "bs": random.randint(1000, 60000)
            },
            {"t": "lf"},
            {"t": "lf"},
            {"t": "lf"},
            {"t": "lf"},
            {"t": "m", "n": "cp-n-8de6c4cf6d6ca5f0"}
        ],
        '02': 1,
        '03': 'b64_string',#b64
        '04': '',
        '05': 3,
        '06': 'yes',
        '07': ()
    }
    _12 = {
        '01': 'b64_string',#b64
        '02': 'yes',
        '03': '',
        '04': 10,
        '05': 3,
        '06': 'generate_true_values_66',
        '07': True,
        '08': random.randint(100, 200),
        '09': True,
        '10': 'a',
        '11': 'undefined',
        '12': 'undefined',
        '13': 'object',
        '14': 'object',
        '15': 'undefined',
        '16': False,
        '17': 'undefined',
        '18': True,
        '20': random.randint(10, 100),
        '21': 0,
        '22': 1,
        '23': True,
        '24': False,
        '25': -1,
        '26': -1,
        '27': '[object Undefined]'
    }
    _13 = {
        '01': 'b64_string',
        '02': 'yes',
        '03': '',
        '01': random.randint(10, 200),
        '02': '', #b64,
        '03': '',
        '04': '3',
        '05': 'yes',
        '06': 'token',
        '07': 'undefined'
    }
    _14 = {
        '01': 'b64_string',
        '02': 'yes',
        '03': '',
        '04': random.randint(100, 500),
        '05': 3,
        '06': 'es-US',
        '07': ["es-US", "es-419", "es"],
        '08': ['es-MX'],
        '09': 'es-es',
        '10': 'diciembre, hora estándar de Colombia',
        '11': 'eo (Ucrania)',
        '12': 'Bippity-boppity, Mumbo-jumbo u hocuspocus',
        '13': '21,000 billones'
    }
    _15 = {
        '01': 'b64_string',
        '02': 'yes',
        '03': '',
        '04': 0,
        '05': 3,
        '06': 'yes'
    }
    _16 = {
        '01': 'b64_string',
        '02': 'unknown_token',
        '03': '',
        '04': random.randint(100, 500),
        '05': 3,
        '06': 2,
        '07': 47
    }
    _17 = {
        '01': 'b64_string',
        '02': 'yes',
        '03': '',
        '04': 2,
        '05': 3,
        '06': 0,
        '07': -296,
        '08': -300,
        '09': -300,
        '10': -300,
        '11': 300,
        '12': 300,
        '13': 'America/Bogota'
    }
    _18 = {
        '01': 'b64_string',
        '02': 'yes',
        '03': '',
        '04': 13,
        '05': 3,
        '06': 'LXAqOBg3OXBhRFAGOS0DDAtGSRQKQDQWTlcUT0NcEmcGKnBuY2UoNxQYClxvVlEdTDMVTlAWT0RfEGETGQZEHFQ7Nxs/P3Jhb0obGxoKC0caSEdfF2MTHgVGGkEIQTFADmFhYG0uNRQzEEFNYVgaAG8UHQVBGEEPQjNGG1IXShIfJhQ8N3Rjb2EBBjg9AkBWFEYMQjREG1UUSBQKFWIWSEVwb24mMxYzO1tQQ28TByNIHFYUTxYKEmEUTlBDGURZAgUzNHxlbWEqHCUfNUlRWBoNEWETTFBEGkZfFzZFHgNUfmElOxAxO3BKXk0kDiQEQFdHGkFdFzFGHAVBTRcPRCEiO39ta2MqNz8CF35YX1ZREDJGGwdBShQNQjQRTVUSWnAqOBg3OXBhRFAGOS0DDAtGSRQKQDQWTlcUT0NcEmcGKnBuY2UoNxQYClxvVlEdTDMVTlAWT0RfEGETGQZEHFQ7Nxs/P3Jhb0obGxoKC0caSEdfF2MTHgVGGkEIQTFADmFhYG0uNRQzEEFNYVgaAG8UHQVBGEEPQjNGG1IXShIfJhQ8N3Rjb2EBBjg9AkBWFEYMQjREG1UUSBQKFWIWSEVwb24mMxYzO1tQQ28TByNIHFYUTxYKEmEUTlBDGURZAgUzNHxlbWEqHCUfNUlRWBoNEWETTFBEGkZfFzZFHgNUfmElOxAxO3BKXk0kDiQEQFdHGkFdFzFGHAVBTRcPRCEiO39ta2MqNz8CF35YX1ZREDJGGwdBShQNQjQRTVUSWnAqOBg3OXBhRFAGOS0DDAtGSRQKQDQWTlcUT0NcEmcGKnBuY2UoNxQYClxvVlEdTDMVTlAWT0RfEGETGQZEHFQ7Nxs/P3Jhb0obGxoKC0caSEdfF2MTHgVGGkEIQTFADmFhYG0uNRQzEEFNYVgaAG8UHQVBGEEPQjNGG1IXShIfJhQ8N3Rjb2EBBjg9AkBWFEYMQjREG1UUSBQKFWIWSEVwb24mMxYzO1tQQ28TByNIHFYUTxYKEmEUTlBDGURZAgUzNHxlbWEqHCUfNUlRWBoNEWETTFBEGkZfFzZFHgNUfmElOxAxO3BKXk0kDiQEQFdHGkFdFzFGHAVBTRcPRCEiO39ta2MqNz8CF35YX1ZREDJGGwdBShQNQjQRTVUSWnAqOBg3OXBhRFAGOS0DDAtGSRQKQDQWTlcUT0NcEmcGKnBuY2UoNxQYClxvVlEdTDMVTlAWT0RfEGETGQZEHFQ7Nxs/P3Jhb0obGxoKC0caSEdfF2MTHgVGGkEIQTFADmFhYG0uNRQzEEFNYVgaAG8UHQVBGEEPQjNGG1IXShIfJhQ8N3Rjb2EBBjg9AkBWFEYMQjREG1UUSBQKFWIWSEVwb24mMxYzO1tQQ28TByNIHFYUTxYKEmEUTlBDGURZAgUzNHxlbWEqHCUfNUlRWBoNEWETTFBEGkZfFzZFHgNUfmElOxAxO3BKXk0kDiQEQFdHGkFdFzFGHAVBTRcPRCEiO39ta2MqNz8CF35YX1ZREDJGGwdBShQNQjQRTVUSWnAqOBg3OXBhRFAGOS0DDAtGSRQKQDQWTlcUT0NcEmcGKnBuY2UoNxQYClxvVlEdTDMVTlAWT0RfEGETGQZEHFQ7Nxs/P3Jhb0obGxoKC0caSEdfF2MTHgVGGkEIQTFADmFhYG0uNRQzEEFNYVgaAG8UHQVBGEEPQjNGG1IXShIfJhQ8N3Rjb2EBBjg9AkBWFEYMQjREG1UUSBQKFWIWSEVwb24mMxYzO1tQQ28TByNIHFYUTxYKEmEUTlBDGURZAgUzNHxlHA=='
    }

class CF_Interactive(OrchestrateJS):
    def __init__(self, js, chl_opts, auto_mode=False):
        self.auto_mode = auto_mode
        self.chl_opts = chl_opts
        super().__init__(code_js=js, auto_mode=self.auto_mode)

        if not self.auto_mode:
            ReversedObjects.cf_chl_opt = {
                'cType': self.find_value(3),
                'cRay': self.find_value(4),
                'cvId': self.find_value(1),
                'cUPMDTk': self.find_value(6).split('__cf_chl_tk=')[1],
                'chlApiTimeoutEncountered': None
            }
        else:
            ReversedObjects.cf_chl_opt.update({
                'chlApiRcV': self.find_value(9),
                'chlApiSitekey': self.find_value(6),
                'cH': self.find_value(16),
                'md': self.find_value(24),
                'chlApiWidgetId': self.find_value(5),
                'chlApiTimeoutEncountered': self.find_value(10),
                'cITimeS': self.find_value(25)
            })
        self.parse_params()

    def generate_equal_data(self,value='window.frameElement', c=2):
        data = []
        for i in range(c):
            data.append(value)
        return data

    def find_value(self, index):
        fr = self.chl_opts[index]

        if '"' in fr:
            return fr.split('"')[1]
        elif "'" in fr:
            return fr.split("'")[1]
        elif ',' and not ("'" in fr or '"' in fr):
            return fr.split(',')[0].strip()

    def perform_now(self) -> tuple[float, float]:
        p1 = reversed_funcs.call('perfom')
        p2 = reversed_funcs.call('perfom')
        print(p1, p2)
        return p1, p2

    def encode_final_chl(self, cf_ray, flow_url, domain, userAgent):
        b64_symbol = random.choice(['==', '='])
        _chl = {k.replace('_', ''): v for k, v in FinalChlParams.__dict__.items() if k[1:2].isnumeric()}
        concat_this = ['wr', 'w6', 'wp', 'w4']

        for payload, values in _chl.items():
            for pnumber, value in values.items():
                if value == 'binascii':
                    _chl[payload][pnumber] = secrets.token_hex(32)

                elif value == 'b64_string':
                    random_bytes = get_random_bytes(12)
                    base64_value = random.choice(concat_this) + base64.b64encode(random_bytes).decode('utf-8')[2:]
                    _chl[payload][pnumber] = base64_value + b64_symbol

                elif value == 'generate_true_values_66':
                    _chl[payload][pnumber] = self.generate_equal_data(value=True, c=66)

                elif isinstance(value, list):
                    for i,l in enumerate(value):
                        if 'n' in value:
                            if l['n'] == 'cp-n-8de6c4cf6d6ca5f0':
                                _chl[payload][pnumber][i]['n'] = f'cp-n-{cf_ray}'
                            elif '/cdn-cgi/challenge-platform/h/b/orchestrate/chl_api' in l['n']:
                                _chl[payload][pnumber][i]['n'] = f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/b/orchestrate/chl_api/v1?ray={cf_ray}&lang=auto'
                            elif '/cdn-cgi/challenge-platform/h/b/flow/ov1' in l['n']:
                                _chl[payload][pnumber][i]['n'] = flow_url

                elif value == 'wbBaseData_values':
                    _chl[payload][pnumber] = wbBaseData(
                        domain=domain.replace('https://', ''),
                        useragent=userAgent
                    )

        print(_chl)
        return _chl

    def invest_data(self, data) -> dict[str, typing.Any]:
        return {k: data[k] for k in reversed(data)}

    def cf1_flow_data(self) -> dict[str, typing.Any]:
        new_flow_data = {}

        eMp1, eMp2 = self.perform_now()
        eMp3, eMp4 = self.perform_now()

        ordered_flow = {
            '01': self.find_value(3),
            '02': self.find_value(1),
            '03': self.find_value(11),
            '04': 0,
            '05': abs(eMp3 - eMp4) if (eMp3 - eMp4) < 0 else eMp3 - eMp4,
            '06': abs(eMp1 - eMp2) if (eMp1 - eMp2) < 0 else eMp1 - eMp2,
            '07': 1,
            '08': self.find_value(8),
            '09': self.find_value(16),
            '10': self.flow_data['unknown_array'],
            '11': False,
            '12': False,
            '13': self.flow_data['ass_param2'],
            '14': '',
            '15': [],#self.generate_equal_data(c=random.randint(2, 3)),
            '16': 0,
            '17': self.flow_data['ass_param1']
        }
        for key, value in zip(self.interactive_data.keys(), ordered_flow.values()):
            new_flow_data[key] = value

        return new_flow_data#self.invest_data(new_flow_data)

    def cf2_flow_data(
        self, 
        domain, 
        parsed_domain, 
        really_key, 
        onload_token,
        flow2_token,
        website_cf_ray
    ):
        new_flow_data = {}

        eMp1, eMp2 = self.perform_now()
        eMp3, eMp4 = self.perform_now()

        ordered_flow = {
            '01': self.find_value(14),
            '02': self.find_value(1),
            '03': 0,
            '04': 0,
            '05': abs(eMp3 - eMp4) if (eMp3 - eMp4) < 0 else eMp3 - eMp4,
            '06': abs(eMp1 - eMp2) if (eMp1 - eMp2) < 0 else eMp1 - eMp2,
            '07': 1,
            '08': self.find_value(25),
            '09': self.find_value(24),
            '10': self.flow_data['unknown_array'],
            '11': 'undefined',
            '12': 'undefined',
            '13': self.flow_data['ass_param1'],
            '14': '',
            '15': self.generate_equal_data(c=2),
            '16': 0,
            '17': self.flow_data['ass_param2'],
            '18': '0',
            '19': self.find_value(6),
            '20': 'interactive',
            '21': website_cf_ray,# self.find_value(15),
            '22': flow2_token,
            '23': 0,
            '24': really_key,
            '25': 'https://{}/turnstile/v0/b/{}/api.js?onload={}&render=explicit'.format(self.find_value(2), really_key, onload_token),
            '26': domain,
            '27': parsed_domain,
            '28': self.find_value(9),
            '29': 28371.339999973774,#random.uniform(10, 500),
            '30': 899.9950000047684,#,random.uniform(10, 500),
            '31': 0,
            '32': 0,
            '33': 863.8199999928474,#random.uniform(10, 500),
            '34': 0,
            '35': 2.615000009536743,#random.uniform(10, 500),
            '36': 53.8649999499321,#random.uniform(10, 500),
            '37': 120.11500000953674,#random.uniform(10, 500),
            '38': 12.415000021457672#andom.uniform(10, 500),
        }
        for key, value in zip(self.interactive_data.keys(), ordered_flow.values()):
            new_flow_data[key] = value
        return new_flow_data

if __name__ == '__main__':
    print(CF_Widget.timestamp())
    #d, b, r = CF_Parser.cf_params('https://nopecha.com/demo/cloudflare',TEST_SITEKEY)

    #for i,v in enumerate(b):
    # ##   print(i, v)
    #c = CF_Solver(
    #    'https://nopecha.com/demo/cloudflare',
    #    siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
    #)
    #auto_mode = True
    #orc = c.cf_orchestrate_js(auto_mode)
    #inte = CF_Interactive(orc, b, auto_mode)

    #a = inte.cf2_flow_data('https://nopecha.com/demo/cloudflare', 'https://nopecha.com')
    #inte.encode_final_chl()
    #print(a)
