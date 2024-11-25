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
node_fetch = require('node-fetch')
PATH = 'cloudflare-data/orchestrate.json'
reversed_funcs = execjs.compile(open('cf_reversed_funcs.js', 'r').read())

class ReversedObjects:
    unknown_array: dict[str, int] = None

class VM_Automation:
    def __init__(self, domain, userAgent, cf_html=False):
        self.domain = domain
        self.userAgent = userAgent
        self.resource_loader = jsdom.ResourceLoader({'userAgent': self.userAgent})
        self.dom_context = None
        self.ov1_contentType = 'application/x-www-form-urlencoded'

        self.window = jsdom.JSDOM(self._cf_create_html(cf_html), {
            'url': self.domain,
            'referrer': self.domain + '/',
            'contentType': 'text/html',
            'includeNodeLocations': True,
            'pretendToBeVisual': True,
            'storageQuota': 10000000,
            'runScripts': 'dangerously',
            'resources': self.resource_loader
        }).getInternalVMContext()

        self.resolutions = (
            (3440,1440,3440,1400),
            (1924,1007,1924,1007),
            (1920,1080,1920,1040),
            (1280,720,1280,672),
            (1920,1080,1920,1032),
            (1366,651,1366,651),
            (1366,768,1366,738),
            (1920,1080,1920,1050)
        )
        self._initialize_window()

    def _initialize_window(self):
        o_height, o_width, i_width, i_height = random.choice(list(self.resolutions))

        self.window.devicePixelRatio = random.uniform(1.2, 1.9)
        self.window.innerHeight = i_height
        self.window.innerWidth = i_width
        self.window.outerHeight = o_height
        self.window.outerWidth = o_width

        self.window.origin = 'https://challenges.cloudflare.com'
        self.window.originAgentCluster = False
        self.window.orientation = 0
        self.window.isSecureContext = True

        self.window.clientInformation = {
            'appCodeName': 'Mozilla',
            'appName': 'Netscape',
            'appVersion': self.userAgent.replace('Mozilla ', ''),
            'cookieEnabled': True,
            'contacts': {},
            'credentials': {},
            'deviceMemory': (1 << random.randint(1, 4)),
            'doNotTrack': None,
            'ink': {},
            'maxTouchPoints': 2,
            'keyboard': {},
            'locks': {},
            'hardwareConcurrency': 8,
            'mimeTypes': {'length': 0},
            'ml': {},
            'bluetooth': {'onadvertisementreceived': None},
            'clipboard': {},
            'connection': {
                'downLink': 3.45,
                'downLinkMax': 100,
                'effectiveType': random.choice(['4g', 'hg', '3g']),
                'onchange': None,
                'ontypechange': None,
                'rtt': 150,
                'saveData': True,
                'type': 'cellular'
            },
            'geolocation': {},
            'gpu': {'wgslLanguageFeatures': {'size': 0}},
            'devicePosture': {
                'onchange': None,
                'type': 'continuous'
            },
            'mediaCapabilities': {},
            'mediaDevices': {},

            'mediaSession': {'metadata': None, 'playbackState': 'none'},
            'plugins': {'length': 0, 'refresh': None},
            'scheduling': {},
            'usb': {'onconnect': None, 'ondisconnect': None},
            'wakeLock': {},
            'webkitPersistentStorage': {},
            'webkitTemporaryStorage': {},
            'onLine': True,
            'pdfViewerEnabled': False,
            'permissions': {},
            'platform': 'Linux armv81',
            'product': 'Gecko',
            'productSub': '20030107',
            'serviceWorker': {
                'controller': None,
                'oncontrollerchange': None,
                'onmessage': None,
                'onmessageerror': None,
                'ready': None
            },
            'storage': {'onquotachange': None},
            'storageBuckets': {},
            'userActivation': {
                'hasBeenActive': True,
                'isActive': False
            },
            'managed': {'onmanagedconfigurationchange': None},
            'presentation': {'defaultRequest': None, 'receiver': None},
            'virtualKeyboard': {}, # <= unknown keyboard
            'xr': {'ondevicechange': None},
            'userAgent': self.userAgent,
            'userAgentData': {
                'brands': [
                    {'brand': 'Not-A.Brand', 'version': '99'},
                    {'brand': 'Chromium', 'version': '124'}
                ],
                'mobile': True,
                'platform': 'Linux'
            },
            'webdriver': False,
            'vendor': 'Google Inc.',
            'vendorSub': ''
        }

    def _cf_create_html(self, html):
        if html:
            # for cf_clearance
            #ray = ClearanceBase.cf_ray
            #timestamp = ClearanceBase.encoded_timestamp

            with open('cloudflare-data/clearance_base.html', 'r') as f:
                html_code = f.read()#.replace('CF_RAY', ray).replace('TIMESTAMP', timestamp)
            print(html_code)
            return html_code
        return ''

    def get_reversed_func(self, func_name='h'):
        with open('cf_reversed_funcs.js', 'r') as f:
            code = f.read()

        if func_name == 'h':
            return code.split('//-')[1].split('//+')[0]
        elif func_name == 'iden':
            return code.split('//@')[1].split('//$')[0]

    def send_ov1_request(self, flowUrl, flowToken, cfChallenge, cfRay):
        self.window.fetch = node_fetch

        vm.Script(self.get_reversed_func()).runInContext(self.window) 
        vm.Script('''
        function cfrequest(flow, encryptedToken, challengeToken, cRay) {
            return new Promise((resolve, reject) => {
                window.fetch(flow, {
                    "headers": {
                        "accept": "*/*",
                        "accept-language": "es-US,es-419;q=0.9,es;q=0.8",
                        "cf-challenge": challengeToken,
                        "cf-chl-retryattempt": "0",
                        "content-type": "ov1_type",
                        "save-data": "on",
                        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
                        "sec-ch-ua-arch": '""',
                        "sec-ch-ua-bitness": '""',
                        "sec-ch-ua-full-version": '"124.0.6327.4"',
                        "sec-ch-ua-full-version-list": '"Not-A.Brand";v="99.0.0.0", "Chromium";v="124.0.6327.4"',
                        "sec-ch-ua-mobile": "?1",
                        "sec-ch-ua-model": '"SM-A032M"',
                        "sec-ch-ua-platform": '"Android"',
                        "sec-ch-ua-platform-version": '"13.0.0"',
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin"
                    },
                    "referrer": "https://nopecha.com/demo/cloudflare",
                    "referrerPolicy": "same-origin",
                    "body": `v_${cRay}=${encryptedToken}`,
                    "method": "POST",
                    "mode": "cors",
                    "credentials": "omit"
                })
                .then(response => response.text())
                .then(data => resolve(data))
            });
        }

        async function wait(u, e, c, r) {
            try {
                const status = await cfrequest(u, e, c, r);
                return status;
            } catch(err) {
                console.log(err)
            }
        }
        '''.replace('ov1_type', self.ov1_contentType)).runInContext(self.window)

        result = vm.Script('''
        wait("url", "encrypted", "_challenge", "_ray")
        '''.replace('url', flowUrl).replace('encrypted', flowToken).replace('_challenge', cfChallenge).replace('_ray', cfRay)).runInContext(self.window)
        print('cloudflare response:', result[:60])
        decrypted = self.decrypt_response(result, cfRay)
        print('decrypted:', decrypted[:90])

    @staticmethod
    def analyze_obf(number, f_less, obf_code, obf_number, parseint_gen, parentesis, _return_c=False):
        codee = '''
        for (
            gF = b,
            (function (c, d, gE, e, f) {
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
                    return jE;
                }),
                a()
            );
        }
        '''.replace('INT_GEN', parseint_gen).replace('FF_LESS', str(f_less)).replace('OBFUSC_CODE', obf_code).replace('OBFUSC_NUMBER', str(obf_number)).replace('PARENTESI', parentesis)
        if _return_c:
            return codee
        vm.Script(codee).runInThisContext()
        result = vm.Script('b(Number(NUMBER))'.replace('NUMBER', str(number))).runInThisContext()
        return result

    def reverse_website_identifier(self) -> dict[typing.Union[int, str], typing.Any]:
        vm.Script(self.get_reversed_func('iden')).runInContext(self.window)
        vm.Script('''
        function ffEge(D, E, F, G) {
            if (E === null || E === void 0)
                return G;
            
            for (
                I = y(E),
                D.Object.getOwnPropertyNames && (I = I.concat(Object.getOwnPropertyNames(E))),
                I = D.Array.from && D.set ? D.Array.set(new D.Set(I)) : function(O, a5, P) {
                    for (
                        O.sort(),
                        P = 0; P < O.length; O[P] === O[P + 1] ? O.splice(P + 1, 1) : P += 1
                    );
                    return O
                }(I),
                J = 'nAsAaAb'.split('A'),
                J = J.includes.bind(J),
                K = 0; K < I.length; L = I[K],
                M = v(D, E, L),
                J(M) ? (N = M === 's' && !D.isNaN(E[L]),
                'd.cookie' === F + L ? H(F + L, M) : N || H(F + L, E[L])) : H(F + L, M), K++
            );
            return G;
            function H(O, P) {
                Object.prototype.hasOwnProperty.call(G, P) || (G[P] = []),
                G[P].push(O)
            }
        }
        function B(){
            try {
                return f = window.document.createElement('iframe'),
                f.style = 'display: none',
                f.tabIndex = '-1',
                window.document.body.appendChild(f),
                D = f.contentWindow,
                E = {},
                E = ffEge(D, D, '', E),
                E = ffEge(D, window.clientInformation || window.navigator, 'n.', E),
                E = ffEge(D, f.contentDocument, 'd.', E),
                window.document.body.removeChild(f),
                F = {},
                F.r = E,
                F.e = null,
                JSON.stringify(F.r)
            } catch(err) {
                return G = {}, G.r = {}, G.e = err, G 
            }
        }
        ''').runInContext(self.window)
        result = str(vm.Script('B()').runInContext(self.window))
        return result

    def decrypt_response(self, response, cf_ray):
        vm.Script('''
        function eO(f, r, m) {
            const _add = (l, m) => l + m;
            const _subtract = (l, m) => l - m;

            for (
                m,
                j = 32,
                l = r + '_' + 0,
                l = l.replace(/./g, function(n, s) {
                    j ^= l.charCodeAt(s)
                }),
                f = window.atob(f),
                k = [],
                i = -1;
                !isNaN(m = f.charCodeAt(++i));
                k.push(String.fromCharCode(_add(_subtract((m & 255) - j, i % 65535), 65535) % 255))
            );
            return k.join('')
        }
        ''').runInContext(self.window)
        result = vm.Script('eO("resp", "ray")'.replace('resp', response).replace("ray", cf_ray)).runInContext(self.window)
        return result

    def emulate_decrypted(self, vm_code):
        vm.Script(vm_code).runInContext(self.window)

    @staticmethod
    def encrypt_flow_data(data, turnkey, enc_code, obf_v, operators, **kwargs):
        vm.Script(VM_Automation.analyze_obf(number=None, **kwargs, _return_c=True)).runInThisContext()
        vm.Script('var fidk = (number) => b(Number(number))'.replace('fidk', obf_v)).runInThisContext()
        vm.Script(operators).runInThisContext()

        vm.Script(enc_code).runInThisContext()
        vm.Script('''
        function h(y, str_key) {
            return g(y, 6, function(z) {   
                return str_key.charAt(z);
            });
        }
        ''').runInThisContext()
        result = vm.Script("h('_payload', '_turnkey')".replace('_payload', data).replace('_turnkey', turnkey)).runInThisContext()
        return result
                
class OrchestrateJS:
    """
    Cloudflare Orchestrate Anaylzer
    """
    def __init__(self, code_js: str, auto_mode: bool) -> None:
        self.js = code_js
        self.is_flow_auto = auto_mode
        self.flow_data = {
            'flow_url': None,
            'ass_param1': None,
            'ass_param2': None,
            'turnstile_siteKey': None,
            'onload_token': None,
            'really_a_key': None,
            'unknown_array': {}
        }
        self._all_int_values: list[int] = []
        self.f_less: typing.Optional[int] = None
        
        self.interactive_data: typing.Any = None
        self.interactive_keys: list[str] = []

        #self.inter_values1: list[int] = []
        self.inter_values: list[str] = [] # confused values

        self.obf_number: int = None
        self.parseInt: str = None
        self.double_parentesis: str = ''
        self.obf_letters = 'ertyuiopsdfghjklzxcvnm'

    def parse_js_storaged_code(self) -> str:
        for i,v in enumerate(self.js.split('function a(')):
            if v[:1].isalpha() and v[2:3] == ')' and len(v.split('~')) > 500:
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

    def find_obf_value(self, number) -> str:
        jp = self.parse_js_storaged_code()

        find_string = VM_Automation.analyze_obf(
            number=number, 
            f_less=self.f_less, 
            obf_code=jp, 
            obf_number=self.obf_number, 
            parseint_gen=self.parseInt,
            parentesis=self.double_parentesis
        )
        return find_string

    def _array_entry_executed(self, code):
        v = None
        code = code.replace("':", "':'").replace(",'", "','").replace('}}', "}'}").replace("'", '"').replace('d={', '{')
        d_json = json.loads(code)

        for value in list(d_json.values()):
            if '(' in value and ')' in value and (value[:1].isalpha() and not value.startswith('function')):
                v = value[:2]
        return v

    def get_encrypter_floats(self) -> str:
        g_func = None
        encrypter_floats_gens = ''

        for i,v in enumerate(self.js.split("'g':function(")):
            if len(v[:35].split(',')) > 15 and 'Object[' in v:
                g_func = v.split("('')},'")[0].split('1.')

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
        #print('cloudflare floats:', encrypter_floats_gens)
        return encrypter_floats_gens[:len(encrypter_floats_gens) - 1]

    def encrypter_array(self, data, _siteKey):
        func_g = None
        b_v = None

        for i,v in enumerate(self.js.split("'g':function(")):
            if len(v[:35].split(',')) > 15 and 'Object[' in v:
                func_g = 'function g(' + v.split(",'j':function")[0]
                b_v = v[:75].split('{if(')[1][:2]
                o_v = v[:75].split('{if(' + f'{b_v}=')[1][:2]
                func_g = func_g.replace(f'{b_v}={o_v},', f'{b_v} = (number) => b(number),')
                break

        for i,v in enumerate(self.js.split("'h':function(")):
            if f',d=' in v[(len(v) - 1570):(len(v) - 1000)] and v.count('function') > 20 and '=String[' in v[(len(v) - 35):len(v)]:
                #print(v[(len(v) - 1570):len(v)])
                #print(v[(len(v) - 1570):len(v)].split(f',d=' + '{'))
                spli1 = v[(len(v) - 1570):len(v)].split(f',d=' + '{')[1]
                spli2 = 'd={' + spli1.split('=String[')[0]
                d_v = spli2[:len(spli2) - 2]
                d_v = d_v.replace(self._array_entry_executed(d_v), b_v)
                break

        result = VM_Automation.encrypt_flow_data(
            data,
            _siteKey,
            func_g, 
            b_v, 
            d_v, 
            f_less=self.f_less,
            obf_code=self.parse_js_storaged_code(),
            obf_number=self.obf_number,
            parseint_gen=self.parseInt,
            parentesis=self.double_parentesis
        )
        #print('this encrypter!', result)
        return result

    def complete_interactive_data(self, I_IntValues, unknown_values) -> None:
        if not self.is_flow_auto:
            for _value in I_IntValues:
                if '(' in _value:
                    s = _value.split('(')
                    for f in s:
                        if f[:1].isnumeric():
                            if '1e3' in f:
                                f = f.replace('1e3', '1000')
                            elif '5e2' in f:
                                f = f.replace('5e2', '500')

                            self._all_int_values.append(int(f.split(')')[0]))

            blud_v1 = self._all_int_values[len(self._all_int_values) -1]
            blud_v2 = self._all_int_values[len(self._all_int_values) -3]

            mybro_v1 = I_IntValues[len(I_IntValues) -1]
            mybro_v2 = I_IntValues[len(I_IntValues) -5]
        else:
            mybro_v1 = I_IntValues[12]
            mybro_v2 = I_IntValues[16]

            blud_v1 = int(mybro_v1.split('(')[1].split(')')[0])
            blud_v2 = int(mybro_v2.split('(')[1].split(')')[0])

        def _find_object_value(value) -> str:
            for i,v in enumerate(self.js.split(value)):
                if v[:2] == "':":
                    fvalue = v[:20].split("),'")[0].split('(')[1]
            
            return self.find_obf_value(fvalue)

        def _object_type(_obj) -> typing.Any:
            if ('[' in _obj and ']' in _obj) and '(' in _obj:
                return []
            elif ('(' in _obj and ')' in _obj) and '[' not in _obj:
                return ''

        p = self.find_obf_value(blud_v1)
        l = self.find_obf_value(blud_v2)

        if isinstance(_object_type(mybro_v1), str):
            self.flow_data['ass_param1'] = p
        else:
            self.flow_data['ass_param1'] = _find_object_value(p)

        if isinstance(_object_type(mybro_v2), str):
            self.flow_data['ass_param2'] = l
        else:
            self.flow_data['ass_param2'] = _find_object_value(l)

        self.encrypter_array('hello xd, { nnxs es gei lol 2998}', self.flow_data['turnstile_siteKey'])

        if ReversedObjects.unknown_array is None:
            for _value in unknown_values:
                lp = self.find_obf_value(_value)
            
                self.flow_data['unknown_array'][lp] = 0
            ReversedObjects.unknown_array = self.flow_data['unknown_array']
        else:
            self.flow_data['unknown_array'] = ReversedObjects.unknown_array

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
            dk = self.js.split('setTimeout,')[_find_index(self.js.split('setTimeout,'))].split('100,g,')[1][:455]
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
                    if len(code) == 65 and ('+' in code and '-' in code):
                        self.flow_data['turnstile_siteKey'] = code

                    if len(code) in [49, 50] and 'explicit' in code:
                        self.flow_data['onload_token'] = code.split('onload=')[1].split('&')[0]
                        self.flow_data['really_a_key'] = code.split('/')[1]

        for i,v in enumerate(self.js.split('f-')):
            if 'e[f]' in v:
                self.f_less = int(v.split(',')[0]) if v.split(',')[0][:2].isnumeric() else 'Fuck you'
                if self.f_less == 'Fuck you':
                    for dd in v.split('e[f]'):
                        print(dd)

        for i,v in enumerate(self.js.split('parseInt(')):
            if '}(' in v[:500]:
                variaba = v.split('}(')[1][:2]
                self.obf_number = int(v.split('}(' + variaba)[1].split('),')[0].strip())

        # unknown array (super obfuscated)
        unk_values = []
        if ReversedObjects.unknown_array is None:
            for i,v in enumerate(self.js.split(']=performance[')):
                if '={}' in v and '=0,' in v:
                    for letter in self.obf_letters:
                        if ('(),' + letter + '={},' + letter + '[') in v and f']={letter}' in v and 'eM[' in v[(len(v) - 22):] and v[:1].isalpha() and v[2:3] == '(':
                            variale = v[:2]
                            v = v.split(letter + '={},')[1].split(f',eM[{variale}')[0]
 
                            for l in v.split(f'{variale}('):
                               if l[:2].isnumeric():
                                    unk_values.append(int(l.split(')')[0]))


        self.parseInt = self.parseInt_values()
        self.interactive_data = self.intauto_values()
        OrchestrateJS.set_orchestrate_data(self.interactive_data)

        _int_keys_l = list(self.interactive_data.keys())
        _int_values_I = list(self.interactive_data.values())
 
        self.complete_interactive_data(_int_values_I, unk_values)

#if __name__ == '__main__':
#    c = CF_Solver(
#        'https://nopecha.com/demo/cloudflare',
#        siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
#    )
#    orc = c.cf_orchestrate_js(False)
#    p = OrchestrateJS(orc, auto_mode=False)
#    p.parse_params()
#    print(p.flow_data)
