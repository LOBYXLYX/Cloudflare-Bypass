import sys
import types
import json
import time
import typing
import random
import string
import execjs
from javascript import require
#from aqua import CF_Solver
#from storage_orchestrate import set_orchestrate_data, get_orchestrate_data

jsdom = require('jsdom')
vm = require('vm')
xml_lib = require('xmlhttprequest')
PATH = 'cloudflare-data/orchestrate.json'
reversed_funcs = execjs.compile(open('cf_reversed_funcs.js', 'r').read())

class CodeFinder:
    def c_variable(js):
        for i,v in enumerate(js.split("setTimeout,")):
            if 'gF,c={' in v:
                c = v.split('gF,c={')[1]
        return c

class VM_Automation:
    def __init__(self, domain, userAgent):
        self.domain = domain
        self.userAgent = userAgent
        self.resource_loader = jsdom.ResourceLoader({'userAgent': self.userAgent})
        self.dom_context = None

        self.content_type = 'text/html'
        self.ov1_contentType = 'application/x-www-form-urlencoded'

    def get_reversed_func(self, func_name='h'):
        with open('cf_reversed_funcs.js', 'r') as f:
            code = f.read()

        if func_name == 'h':
            return code.split('//-')[1].split('//+')[0]

    def send_ov1_request(self, flowUrl, flowToken, cfChallenge, cfRay):
        print(flowUrl)
        if self.dom_context is None:
            self.dom_context = jsdom.JSDOM('', {
                'url': self.domain,
                'contentType': self.content_type,
                'includeNodeLocations': True,
                'pretendToBeVisual': True,
                'storageQuota': 10000000,
                'runScripts': 'dangerously',
                'resources': self.resource_loader
            }).getInternalVMContext()
            
            self.dom_context.XMLHttpRequest = xml_lib.XMLHttpRequest

        vm.Script(self.get_reversed_func()).runInContext(self.dom_context)
    
        vm.Script('''
        function cfrequest(flow, encryptedToken, challengeToken, cfRay) {
            return new Promise((resolve, reject) => {
                x = new window.XMLHttpRequest(),
                console.log(x),
                console.log(flow),

                x.open('POST', flow, true),
                x.timeout = 2500 * (1 + 0),
                x.ontimeout = function(){
                    h()
                },
                x.setRequestHeader('Content-Type', 'ov1_type'),
                x.setRequestHeader('CF-Challenge', challengeToken),
                x.onreadystatechange = function() {
                    if (l = '600010', x.readyState != 4)
                        return;
                    if (x.status != 200 && x.status != 304)
                        return;
                },
                x.onload = function() {
                    resolve(x.status);
                },
                console.log(flow),
                console.log(`v_${cfRay}=${encryptedToken}`),
                x.send(`v_${cfRay}=${encryptedToken}`)
            });
        }
        async function wait(u, e, c, r) {
            try {
                const status = await cfrequest(u, e, c, r);
                console.log(status);
            } catch(err) {
                console.log(err)
            }
        }
        '''.replace('ov1_type', self.ov1_contentType)).runInContext(self.dom_context)

        vm.Script('''
        wait("url", "encrypted", "_challenge", "_ray")
        '''.replace('url', flowUrl).replace('encrypted', flowToken).replace('_challenge', cfChallenge).replace('_ray', cfRay)).runInContext(self.dom_context)

    @staticmethod
    def analyze_obf(number, f_less, obf_code, obf_number, parseint_gen, parentesis):
        codee = '''
        for (
            gF = b,
            console.log('before'),
            (function (c, d, gE, e, f) {
                console.log('before 2', c, d)
                for (gE = b, e = c(); !![]; )
                    try {
                        if (
                            PARENTESIf = INT_GEN f === d)
                            break;
                        else e.push(e.shift());
                    } catch (g) {
                        e.push(e.shift());
                    }
                })(a, OBFUSC_NUMBER),
                eZ = [],
                f0 = 0;
            256 > f0;
            eZ[f0] = String.fromCharCode(f0), f0++
        );
        function b(c, d, e) {
            return (
                (e = a()),
                //console.log(e),
                (b = function (f, g, h) {
                    return (f = f - FF_LESS), (h = e[f]), h;
                }),
                b(c, d)
            );
        }
        function a(jE) {
            return (
                (jE = 'OBFUSC_CODE'.split(
                    "~"
                )),
                (a = function () {
                    //console.log(jE);
                    return jE;
                }),
                a()
            );
        }
        '''.replace('INT_GEN', parseint_gen).replace('FF_LESS', str(f_less)).replace('OBFUSC_CODE', obf_code).replace('OBFUSC_NUMBER', str(obf_number)).replace('PARENTESI', parentesis)
        print(codee)
        vm.Script(codee).runInThisContext()
        result = vm.Script('b(Number(NUMBER))'.replace('NUMBER', str(number))).runInThisContext()
        print(result)
        

class OrchestrateJS:
    """
    Reverse Engineering Cloudflare Javascript
    """
    def __init__(self, code_js: str, auto_mode: bool) -> None:
        self.js = code_js
        self.is_flow_auto = auto_mode
        self.flow_data = {
            'flow_url': None,
            'ass_param1': self._random_string(6),
            'ass_param2': self._random_string(random.randint(5, 6)),
            'turnstile_siteKey': None,
            'onload_token': None,
            'really_a_key': None
        }
        self._all_int_values: list[int] = []
        self.f_less: typing.Optional[int] = None
        
        self.interactive_data: typing.Any = None
        self.interactive_keys: list[str] = []
        self.interactive_values: list[int] = []
        self.obf_number: int = None
        self.parseInt: str = None
        self.double_parentesis: str = ''

    def parse_js_storaged_code(self) -> str:
        for i,v in enumerate(self.js.split('function a(')):
            if v[:2].isalpha() and v[2:3] == ')' and len(v.split('~')) > 500:
                variable = v[:2]
                d = v.split(f"return {variable}='")[1].split('.split(')[0]

        if d[(len(d) - 1):len(d)] == "'":
            d = d.replace("'", '')
        return d

    @staticmethod
    def set_orchestrate_data(values):
        data = {'interactive_1': values}
        with open(PATH, 'w') as f: json.dump(data, f, indent=4)

    @staticmethod
    def get_orchestrate_data(key='interactive_1') -> typing.Any:
        with open(PATH, 'r') as f:
            data = json.load(f)
        return data.get(key, None)

    def _random_string(self, length) -> str:
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(length)])

    def _find_int_value(self, number) -> str:
        jp = self.parse_js_storaged_code()
        print(jp)
        print(self.f_less, number, self.obf_number, type(jp))

        VM_Automation.analyze_obf(
            number=number, 
            f_less=self.f_less, 
            obf_code=jp, 
            obf_number=self.obf_number, 
            parseint_gen=self.parseInt,
            parentesis=self.double_parentesis
        )
        return find_n

    def get_encrypter_floats(self) -> str:
        g_func = None
        encrypter_floats_gens = ''

        for i,v in enumerate(self.js.split("'g':function(")):
            if len(v[:35].split(',')) > 15 and 'Object[' in v:
                g_func = v.split("('')},'")[0].split('1.')
                print(v.split("('')},'")[0])

        # wb method
        for i, v in enumerate(g_func):
            if v[:2].isnumeric() or v[:1].isnumeric():
                parsed_length = 2 if v[:2].isnumeric() else 1
                encrypter_floats_gens += '1.' + v[:parsed_length] + ','

            if v[:3] == '1|1' and (v[:4].split('|')[1].isnumeric() or v[:5].split('|')[1].isnumeric()):

                parsed_length = 4 if v[:4].split('|')[1].isnumeric() else 5
                encrypter_floats_gens += '1.' + v[:parsed_length].split('|')[1] + ',' 
        while not len(encrypter_floats_gens.split(',')) > 6:
            encrypter_floats_gens += str(round(random.uniform(1, 1.99), random.randint(1, 2))) + ','
        #print('Encryptor Floats:', encrypter_floats_gens)
        return encrypter_floats_gens[:len(encrypter_floats_gens) - 1]

    def complete_interactive_data(self, I_IntValues) -> None:
        for _value in I_IntValues:
            if '(' in _value:
                s = _value.split('(')
                for f in s:
                    if f[:1].isnumeric():
                        self._all_int_values.append(int(f.split(')')[0]))

        self.interactive_values.append(self._all_int_values[len(self._all_int_values)-1])
        self.interactive_values.append(self._all_int_values[len(self._all_int_values)-3])
        print(self.interactive_values)

        self._find_int_value(self.interactive_values[1])

    def intauto_values(self) -> dict[str, str]:
        def _find_index(js):
            for i,v in enumerate(js):
                if ('100,g,' in v or '100,e,' in v):
                    return i

        # bypass dinamic code
        if self.is_flow_auto:
            dk = self.js.split('setTimeout(')[_find_index(self.js.split('setTimeout('))].split('100,e,')[1][:1265]
            if ']})' in dk:
                dk = dk.split(']})')[0] + ']}'
            elif ')})' in dk:
                dk = dk.split(')})')[0] + ')}'
        else:
            dk = self.js.split('setTimeout,')[_find_index(self.js.split('setTimeout,'))].split('100,g,')[1][:445]
            if ']})' in dk:
                dk = dk.split(']})')[0] + ']}'
            elif ')})' in dk:
                dk = dk.split(')})')[0] + ')}'
        return json.loads(dk.replace(':', ":'").replace(",'", "','").replace("}", "'}").replace("''''", "''").replace("'", '"'))

    def parseInt_values(self) -> str:
        # This Is Hard Asf
        spli1 = self.js.split('(f=')[1].split('.push(')[0].split('===')[0]

        test = spli1.replace('\n', '').replace(' ', '')
        if '),' in test[(len(test) - 5):len(test)]:
            spli2 = (spli1.split('),')[0] + '),')
            #self.double_parentesis = '('

        elif ',' in test[(len(test) - 5):len(test)]:
            spli2 = (spli1.split(',')[0] + ',')

        spli2 = spli2.replace('\n', '').strip().replace(' ', '')

        variable = spli2.split('parseInt(')[1][:2]
        _parseInt = spli2.replace(variable, 'gE')
        return _parseInt

    def parse_params(self):
        for i,v in enumerate(self.js.split('~/')):
            if len(v.split(':')) > 2:
                js2 = v.split('/~')
                for s in js2:
                    if str(round(time.time()))[:5] in s and len(s.split(':')) == 3:
                        self.flow_data['flow_url'] = s

        for i,v in enumerate(self.js.split("='")):
            if len(v.split('~')) > 500:
                for code in v.split('~'):
                    if len(code) == 65:
                        self.flow_data['turnstile_siteKey'] = code

                    if len(code) in [49, 50] and 'explicit' in code:
                        self.flow_data['onload_token'] = code.split('onload=')[1].split('&')[0]
                        self.flow_data['really_a_key'] = code.split('/')[1]

        for i,v in enumerate(self.js.split('f-')):
            if 'e[f]' in v:
                self.f_less = int(v.split(',')[0]) if v.split(',')[0][:3].isnumeric() else 'Fuck you'

        for i,v in enumerate(self.js.split('parseInt(')):
            if '}(' in v[:500]:
                variaba = v.split('}(')[1][:2]
                self.obf_number = int(v.split('}(' + variaba)[1].split('),')[0].strip())
                print(self.obf_number)

        self.parseInt = self.parseInt_values()
        print(self.parseInt)
        self.interactive_data = self.intauto_values()
        print(self.interactive_data)
        OrchestrateJS.set_orchestrate_data(self.interactive_data)

        _int_keys_l = list(self.interactive_data.keys())
        _int_values_I = list(self.interactive_data.values())
 
        self.complete_interactive_data(_int_values_I)

if __name__ == '__main__':
    c = CF_Solver(
        'https://nopecha.com/demo/cloudflare',
        siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
    )
    orc = c.cf_orchestrate_js(False)
    p = OrchestrateJS(orc, auto_mode=False)
    p.parse_params()
    print(p.flow_data)
