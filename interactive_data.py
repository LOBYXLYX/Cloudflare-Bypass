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
    
        rep2 = client.get(f'https://challenges.cloudflare.com/cdn-cgi/challenge-platform/h/g/turnstile/if/ov2/av0/rcv0/0/auvka/{siteKey}/dark/fbE/normal/auto/')
        b = rep2.text.split(': ')
        return d[28:len(d)], b[1:len(b)], ray


class CF_Interactive(OrchestrateJS):
    def __init__(self, js, chl_opts, auto_mode=False):
        self.auto_mode = auto_mode
        self.chl_opts = chl_opts
        super().__init__(code_js=js, auto_mode=self.auto_mode)

        if not self.auto_mode:
            ReversedObjects.cf_chl_opt.update({
                'cType': self.find_value(3),
                '_cRay': self.find_value(4),
                'cvId': self.find_value(1),
                'cFPWv': 'g',
                'cUPMDTk': self.find_value(6).split('__cf_chl_tk=')[1],
                'chlApiTimeoutEncountered': None
            })
        else:
            ReversedObjects.cf_chl_opt.update({
                'cRay': self.find_value(15),
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

    def cf1_flow_data(self) -> dict[str, typing.Any]:
        new_flow_data = {}

        eMp1, eMp2 = self.perform_now()
        eMp3, eMp4 = self.perform_now()

        ordered_flow = {
            '01': self.find_value(3),
            '02': self.find_value(1),
            '03': self.find_value(11),
            '04': 0,
            '05': (abs(eMp3 - eMp4) if (eMp3 - eMp4) < 0 else eMp3 - eMp4) * 20,
            '06': (abs(eMp1 - eMp2) if (eMp1 - eMp2) < 0 else eMp1 - eMp2) * 20,
            '07': 1,
            '08': self.find_value(8),
            '09': self.find_value(16),
            '10': self.flow_data['unknown_array'],
            '11': False,
            '12': False,
            '13': self.flow_data['ass_param2'],
            '14': '',
            '15': [], #self.generate_equal_data(c=random.randint(2, 3)),
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
            '05': (abs(eMp3 - eMp4) if (eMp3 - eMp4) < 0 else eMp3 - eMp4) * 20,
            '06': (abs(eMp1 - eMp2) if (eMp1 - eMp2) < 0 else eMp1 - eMp2) * 20,
            '07': 1,
            '08': self.find_value(25),
            '09': self.find_value(24),
            '10': self.flow_data['unknown_array'],
            '11': 'undefined',
            '12': 'undefined',
            '13': self.flow_data['ass_param1'],
            '14': '',
            '15': self.generate_equal_data(c=random.randint(2, 6)),
            '16': 0,
            '17': self.flow_data['ass_param2'],
            '18': '0',
            '19': self.find_value(6),
            '20': 'interactive',
            '21': website_cf_ray,# self.find_value(15),
            '22': flow2_token,
            '23': 0,
            '24': really_key,
            '25': 'https://{}/turnstile/v0/g/{}/api.js?onload={}&render=explicit'.format(self.find_value(2), really_key, onload_token),
            '26': domain,
            '27': parsed_domain,
            '28': self.find_value(9),
            '29': random.uniform(500, 3000),
            '30': random.uniform(500, 1500),
            '31': 0,
            '32': 0,
            '33': random.uniform(300, 1200),
            '34': 0,
            '35': random.uniform(1, 80),
            '36': random.uniform(5, 150),
            '37': random.uniform(100, 600),
            '38': random.uniform(5, 90),
        }
        for key, value in zip(self.interactive_data.keys(), ordered_flow.values()):
            new_flow_data[key] = value

        ReversedObjects.cf_chl_opt['chlApiU'] = ordered_flow['25']
        return new_flow_data

    def cf3_flow_data(self, interactive):
        new_flow_data = {}

        ordered_flow = {
            '01': '',
            '02': self.find_value(15),
            '03': self.find_value(1),
            '04': 0,
            '05': 0,
            '06': '',
            '07': '',
            '08': self.find_value(25),
            '09': '',
            '10': self.flow_data['unknown_array'],
            '11': 1,
            '00': 'undefined',
            '12': '0',
            '13': self.find_value(6),
            '14': 'interactive',
            '15': website_cf_ray,
            '16': '',
            '17': 0,
            '18': really_key,
            '19': 'https://{}/turnstile/v0/g/{}/api.js?onload={}&render=explicit'.format(self.find_value(2), really_key, onload_token),
            '200': domain,
            '21': parsed_domain,
            '22': self.find_value(9),
            '20': random.uniform(10, 1000),
            '24': random.uniform(10, 1000),
            '25': 0,
            '26': 0,
            '27': random.uniform(1000, 10000),
            '28': 0,
            '29': random.uniform(1000, 10020),
            '31': random.uniform(100, 1500),
            '33': random.uniform(40, 400),
            '34': random.uniform(10, 200),
            '35': self.flow_data['ass_param2'],
            '36': 'undefined',
            '00': '',
            '37': '',
            '39': '',
        }
        for key, value in interactive.items():
            for key2, value2 in zip(interactive.keys(), ordered_flow.values()):
                new_flow_data[key]

    def cf4_flow_data(
        self,
        domain,
        parsed_domain,
        really_key,
        onload_token,
        website_cf_ray
    ):
        new_flow_data = {}

        eMp1, eMp2 = self.perform_now()
        eMp3, eMp4 = self.perform_now()

        ordered_flow = {
            '01': self.find_value(14),
            '02': '3',
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
            '15': self.generate_equal_data(c=random.randint(2,3)),
            '16': 0,
            '17': self.flow_data['ass_param2'],
            '18': '0',
            '19': self.find_value(6),
            '20': 'undefined',
            '21': 'undefined',
            '22': 'undefined',
            '23': 0,
            '24': really_key,
            '25': 'https://{}/turnstile/v0/g/{}/api.js?onload={}&render=explicit'.format(self.find_value(2), really_key, onload_token),
            '26': domain,
            '27': parsed_domain,
            '28': self.find_value(9),
            '29': random.uniform(100, 1000),
            '30': random.uniform(500, 1500),
            '31': 0,
            '32': 0,
            '33': random.uniform(300, 1200),
            '34': 0,
            '35': random.uniform(1,80),
            '36': random.uniform(5, 150),
            '37': random.uniform(100, 600),
            '38': random.uniform(5, 90)
        }
        for key, value in zip(self.interactive_data.keys(), ordered_flow.values()):
            new_flow_data[key] = value
        return new_flow_data


    @staticmethod
    def eventClick_data() -> dict[str, str]:
        return {
            'activeElement': '[object HTMLBodyElement]',
            'clientX': '',
            'clientY': '',
            'height': '1',
            'isPrimary': 'false',
            'isTrusted': 'true',
            'layerX': '',
            'layerY': '',
            'movementX': '0',
            'movementY': '0 ',
            'offsetX': '',
            'offsetY': '',
            'pageX': '',
            'pageY': '',
            'pointerId': '2',
            'pointerType': 'touch',
            'pressure': '0',
            'relatedTarget': 'null',
            'screenX': '',
            'screenY': '',
            'srcElement': '[object HTMLInputElement]',
            'targentialPressure': '',
            'target': '[object HTMLInputElement]',
            'timeStamp': str(reversed_funcs.call('perfom') * 1000),
            'type': 'click',
            'width': '1',
            'x': '',
            'y': ''
        }


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
