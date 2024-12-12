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
node_atob = require('atob')
#node_worker = require('web-worker')

PATH = 'cloudflare-data/orchestrate.json'
reversed_funcs = execjs.compile(open('cf_reversed_funcs.js', 'r').read())

cK = 'b'

class ReversedObjects:
    unknown_array: dict[str, int] = None
    challenge_website: str = None
    challenge_cloudflare: str = None
    cf_chl_opt: dict[str, typing.Any] = {}
    chl_opt_keys: dict[str, typing.Any] = {
        'what_hello': {}, 
        'other': [],
        '_setTimeout': []
    }
    initialized_onload: bool = False
    decrypt_presicion: float = 255

class VM_Automation:
    def __init__(self, domain, userAgent, cf_html=False, html_code=None):
        self.domain = domain
        self.userAgent = userAgent
        self.resource_loader = jsdom.ResourceLoader({'userAgent': self.userAgent})
        self.dom_context = None
        self.ov1_contentType = 'application/x-www-form-urlencoded'
        self.html_code = html_code

        self.window = jsdom.JSDOM(self._cf_create_html(cf_html, html_code), {
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

    def _initialize_window(self) -> None:
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

    def _cf_create_html(self, html, code) -> str:
        if html:
            if code is not None:
                return code
            # for cf_clearance
            #ray = ClearanceBase.cf_ray
            #timestamp = ClearanceBase.encoded_timestamp

            with open('cloudflare-data/clearance_base.html', 'r') as f:
                html_code = f.read()#.replace('CF_RAY', ray).replace('TIMESTAMP', timestamp)
            return html_code
        return ''

    def get_reversed_func(self, func_name='h') -> str:
        with open('cf_reversed_funcs.js', 'r') as f:
            code = f.read()

        if func_name == 'h':
            return code.split('//-')[1].split('//+')[0]
        elif func_name == 'iden':
            return code.split('//@')[1].split('//$')[0]

    def send_ov1_request(self, flowUrl, flowToken, cfChallenge, cfRay, referrer) -> str:
        self.window.fetch = node_fetch
        print('cloudflare challenge URL:\033[36m', flowUrl, '\033[0m')
        print('request payload:', f'v_{cfRay}={flowToken[:80]}....')

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
                        "sec-ch-ua-platform-version": '"13.0.0"',
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin"
                    },
                    "referrer": "_referrer_",
                    "referrerPolicy": "same-origin",
                    "body": `v_${cRay}=${encryptedToken}`,
                    "method": "POST",
                    "mode": "cors",
                    "credentials": "omit"
                })
                .then(response => response.text())
                .then(data => {
                    var response_status = true;
                    if (data.includes(`"err"`)) response_status = false;
                    resolve(JSON.stringify({
                        success: response_status,
                        encrypted: data
                    }))
                })
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
        '''.replace('ov1_type', self.ov1_contentType).replace('_referrer_', referrer)).runInContext(self.window)

        result = json.loads(vm.Script('''
        wait("url", "encrypted", "_challenge", "_ray")
        '''.replace('url', flowUrl).replace('encrypted', flowToken).replace('_challenge', cfChallenge).replace('_ray', cfRay)).runInContext(self.window))
        print('cloudflare response:\033[32m', result['encrypted'][:100]+'....', '\033[0m')

        if not result['success']:
            raise TypeError(f'Cloudflare Challenge Failed ({result["encrypted"]})')
        window_decrypted = self.decrypt_response(result['encrypted'], cfRay)

        #if 'challenges' in flowUrl:
        #    open('cloudflare-data/decrypted.js', 'w').write(window_decrypted)
        print('decrypted:', window_decrypted[:90])
        #sys.exit()
        return window_decrypted

    @staticmethod
    def analyze_obf(number, f_less, obf_code, obf_number, parseint_gen, parentesis, _return_c=False, split_type='~') -> str:
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
                    "_blud_this"
                )),
                (a = function () {
                    return jE;
                }),
                a()
            );
        }
        '''.replace('INT_GEN', parseint_gen).replace('FF_LESS', str(f_less)).replace('OBFUSC_CODE', obf_code).replace('OBFUSC_NUMBER', str(obf_number)).replace('PARENTESI', parentesis).replace('_blud_this', split_type)
        if _return_c:
            return codee
        vm.Script(codee).runInThisContext()
        result = vm.Script('b(Number(NUMBER))'.replace('NUMBER', str(number))).runInThisContext()
        return result

    def reverse_website_identifier(self, _return_c=False) -> dict[typing.Union[int, str], typing.Any]:
        vm.Script(self.get_reversed_func('iden')).runInContext(self.window)
        codee = '''
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
        '''
        if _return_c:
            return codee

        vm.Script(codee).runInContext(self.window)
        result = str(vm.Script('B()').runInContext(self.window))
        return result

    def decrypt_response(self, response, cf_ray) -> str:
        self.window.custom_atob = node_atob

        vm.Script('''
        var eO = function(f, r, m) {
            const _add = (l, m) => l + m;
            const _subtract = (l, m) => l - m;

            for (
                m,
                j = 32,
                l = r + '_' + 0,
                l = l.replace(/./g, function(n, s) {
                    j ^= l.charCodeAt(s)
                }),
                f = window.custom_atob(f),
                k = [],
                i = -1;
                !isNaN(m = f.charCodeAt(++i));
                k.push(String.fromCharCode(_add(_subtract((presicion & m) - j, i % 65535), 65535) % 255))
            );
            return k.join('')
        }
        '''.replace('presicion', str(ReversedObjects.decrypt_presicion))).runInContext(self.window)
        result = vm.Script('eO("resp", "ray")'.replace('resp', response).replace("ray", cf_ray)).runInContext(self.window)
        return result

    def undefined(self, array) -> str:
        vm.Script('''
        var modified = {};
        var i = () => undefined;

        Object.entries(_array).forEach(([k, v]) => {
            if (v === 'undefined') {
                v = i();
            }
            modified[k] = v
        })
        '''.replace('_array', array)).runInThisContext()
        result = vm.Script('JSON.stringify(modified)').runInThisContext()
        return result

    def onload_postMessage(self, code, data: dict[str, typing.Any]):
        vm.Script(code).runInContext(self.window)
        vm.Script('window.parent.postMessage(__, "*")'.replace('__', json.dumps(data))).runInContext(self.window)

    @staticmethod
    def encrypt_flow_data(data, turnkey, enc_code, obf_v, operators, split_type='~', **kwargs) -> str:
        vm.Script(VM_Automation.analyze_obf(number=None, **kwargs, _return_c=True, split_type=split_type)).runInThisContext()
        vm.Script('var fi = (number) => b(Number(number))'.replace('fi', obf_v)).runInThisContext()
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

    def evaluate(
        self,
        code: str, 
        decryptedChl: str, 
        flow_auto: bool = False,
        previous_data: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        sendRequest = lambda arg1, arg2: ''

        self.window.decryptedChl = decryptedChl
        self.window._cf_chl_opt = ReversedObjects.cf_chl_opt
        self.window.sendRequest = sendRequest
        self.window._o_k = ReversedObjects.chl_opt_keys['what_hello']
        self.window._o_s = ReversedObjects.chl_opt_keys['_setTimeout']
        
        _0xL = self.window._o_k['fragment']

        # why jsdom doesnt have Blob, URL and TextEncoder?
        self.window.Blob = vm.Script('Blob').runInThisContext()
        self.window.URL = vm.Script('URL').runInThisContext()
        self.window.TextEncoder = vm.Script('TextEncoder').runInThisContext()
        #self.window.Worker = node_worker

        #print(ReversedObjects.chl_opt_keys)

        def _parse_window_eval():
            nonlocal code

            t = code.split(".screen.orientation,'so.',")[1].split('var d={};d=')[1].split('(')[0]
            code = code.replace(t, 'ffEge')

        if flow_auto:
            vm.Script('''
            var mockCanvas = (window) => {
                window.HTMLCanvasElement.prototype.getContext = function () {
                    return {
                        fillRect: function() {},
                        clearRect: function(){},
                        getImageData: function(x, y, w, h) {
                            return  {
                                data: new Array(w*h*4)
                            };
                        },
                        putImageData: function() {},
                        createImageData: function(){ return []},
                        setTransform: function(){},
                        drawImage: function(){},
                        save: function(){},
                        fillText: function(){},
                        restore: function(){},
                        beginPath: function(){},
                        moveTo: function(){},
                        lineTo: function(){},
                        closePath: function(){},
                        stroke: function(){},
                        translate: function(){},
                        scale: function(){},
                        rotate: function(){},
                        arc: function(){},
                        fill: function(){},
                        measureText: function(){
                            return { width: 0 };
                        },
                        transform: function(){},
                        rect: function(){},
                        clip: function(){},
                    };
                }
                window.HTMLCanvasElement.prototype.toDataURL = function () {
                    return "";
                }
            }
            var contain = window.document.createElement('div')
            window.document.body.appendChild(contain);
        
            var _l = {'mode': 'closed'};
            var _shadow = contain.attachShadow(_l);
            _shadow.innerHTML = `__htmlc`

            window._cf_chl_opt[window._o_k['fragment']] = _shadow

            Object.entries(_prev_d).forEach(([k, v]) => {
                window._cf_chl_opt[k] = v
            })

            mockCanvas(window)
            '''.replace('__htmlc', self.html_code).replace('_prev_d', previous_data)).runInContext(self.window)

            vm.Script(self.reverse_website_identifier(True)).runInContext(self.window)
            _parse_window_eval()

        c = code.replace('arguments[0]', 'JSON.parse(window.decryptedChl)').replace('arguments[1]', 'window.sendRequest').replace('URL.createObjectURL', 'window.URL.createObjectURL').replace('new Worker(_cf_chl_ctx.hSNV0)', 'null').replace('document.body ', 'true').replace('document.body.shadowRoot === null', 'true').replace("window._cf_chl_opt.{_0xL}.mode === 'closed'", 'true').replace('document.head.compareDocumentPosition(document.body)', 'true').replace(f"window._cf_chl_opt.{_0xL}.querySelector('style').compareDocumentPosition(window._cf_chl_opt.{_0xL}.querySelector('div')) & Node.DOCUMENT_POSITION_FOLLOWING", 'true').replace(f"document.body.compareDocumentPosition(window._cf_chl_opt.{_0xL}.querySelector('div')) & (Node.DOCUMENT_POSITION_DISCONNECTED | Node.DOCUMENT_POSITION_FOLLOWING | Node.DOCUMENT_POSITION_IMPLEMENTATION_SPECIFIC)", 'true').replace('TextEncoder', 'window.TextEncoder')
        #print(c)

        vm.Script(c).runInContext(self.window)
        if flow_auto:
            #vm.Script('console.log(_cf_chl_opt)').runInContext(self.window)
            #vm.Script('console.log(_cf_chl_ctx)').runInContext(self.window)
            #vm.Script('console.log(Object.keys(_cf_chl_ctx).length - _cf_chl_ctx.lnrK5)').runInContext(self.window)
            vm.Script('''
            Object.entries(JSON.parse(_prev_data)).forEach(([k, v]) => {
                if ((_cf_chl_ctx[k] === undefined || isNaN(_cf_chl_ctx[k]) || _cf_chl_ctx[k] === null) && Object.prototype.hasOwnProperty.call(_cf_chl_ctx, k)) {
                    _cf_chl_ctx[k] = v
                }
            })
            '''.replace('_prev_data', json.dumps(previous_data))).runInContext(self.window)
            vm.Script('console.log(_cf_chl_ctx)').runInContext(self.window)

        result = json.loads(vm.Script('JSON.stringify(_cf_chl_ctx)').runInContext(self.window))
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
        return (v or code)

    def settimeout_find_values(self):
        func_name = None

        for i,v in enumerate(self.js.split('}):setTimeout(')):
            if v[:1].isalpha() and v[2:3] == ',' and v[3:6] == '0),':
                func_name = v[:2]

        for i,v in enumerate(self.js.split(f'function {func_name}(')):
            if 'eN[' in v[:275] and v[:len(v.split('}function')[0])].count('eM[') >= 3:
                calc = len(v.split('}function')[0])
                func = v[:(calc + 15)].split('}function ')[0]

                for v in func.split(']['):
                    if v[2:3] == '(' and "('|')" not in v[:25]:
                        ReversedObjects.chl_opt_keys['_setTimeout'].append(
                            self.find_obf_value(v.split('(')[1].split(')')[0]))

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
            #print('CCCCVVVVVVPPPPP____', v[:400])
            if len(v[:35].split(',')) > 10 and 'Object[' in v:
                func_g = 'function g(' + v.split(",'j':function")[0]
                b_v = v[:115].split('{if(')[1][:2]
                #print('BBBBBBBBVVVVVVVVVVVVV', b_v)
                o_v = v[:115].split('{if(' + f'{b_v}=')[1][:2]
                func_g = func_g.replace(f'{b_v}={o_v},', f'{b_v} = (number) => b(number),')
                break

        for i,v in enumerate(self.js.split("'h':function(")):
           # print('ccccVVVVV', v[(len(v) - 2110):(len(v) - 900)])
            if ",d={'" in v[(len(v) - 2110):(len(v) - 900)] and v.count('function') > 10 and '=String[' in v[(len(v) - 35):len(v)]:
                #print(v[(len(v) - 1570):len(v)])
                #print(v[(len(v) - 1570):len(v)].split(f',d=' + '{'))
                spli1 = v[(len(v) - 2110):len(v)].split(f',d=' + '{')[1]
                spli2 = 'd={' + spli1.split('=String[')[0]
                #print('DDDDDDDDDDARRAY', spli2)
                d_v = spli2[:len(spli2) - 2]
                #print('COMPAREEEEEEE', d_v, b_v)
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

    @staticmethod
    def extract_decrypted_data(code, flow_auto) -> dict[str, typing.Any]:
        window_data = {
            'flow2_token': None,
            'flow2_sendRequest': None,
            'challenge_pat': None,
        }
        if not flow_auto:
            f1 = code.split('var a=_cf_chl_ctx[_cf_chl_ctx')[0].split(']= 0;')[0].split("= '")
            chlpagedata = f1[len(f1) - 1].split("';")[0]

            window_data['flow2_token'] = chlpagedata
            final = code.split("sendRequest('/cdn-cgi/challenge-platform/'+v+'")[1].split(', _cf_')[0]
            window_data['flow2_sendRequest'] = final

            ReversedObjects.cf_chl_opt.update({
                'chlApiChlPageData': chlpagedata,
                'chlApiAppareance': 'always',
                'chlApiExecution': 'render',
                'chlApiExpiryInterval': 290000,
                'chlApiFailureFeedbackEnabled': False,
                'chlApiLanguage': 'auto',
                'chlApiLoopFeedbackEnabled': False,
                'chlApiMode': 'managed',
                'chlApiRefreshExpired': 'never',
                'chlApiRefreshTimeout': 'never',
                'chlApiRetry': 'never',
                'cType': 'chl_api_m'
            })
        else:
            pa = code.split("fetch('/cdn-cgi/challenge-platform' + v + '/")[1].split("', {")[0]
            window_data['challenge_pat'] = pa
        return window_data

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

        self.settimeout_find_values()

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

        ReversedObjects.cf_chl_opt['chlApiACCH'] = self.flow_data['really_a_key']


    def intauto_values(self) -> dict[str, str]:
        def _find_index(js):
            for i,v in enumerate(js):
                if ',100,' in v and 'performance[' and v:
                    return i

        # bypass dinamic code
        if self.is_flow_auto:
            dk = self.js.split('setTimeout(')[_find_index(self.js.split('setTimeout('))].split(',100,')[1]
            dk = '{' + dk.split(',{')[1][:1265]

            if ']})' in dk:
                dk = dk.split(']})')[0] + ']}'
            elif ')})}' in dk:
                dk = dk.split(')})}')[0] + ')}'
            elif ')})' in dk:
                dk = dk.split(')})')[0] + ')}'
        else:
            dk = self.js.split('setTimeout,')[_find_index(self.js.split('setTimeout,'))].split(',100,')[1]
            dk = '{' + dk.split(',{')[1][:455]
    
            if ']})' in dk:
                dk = dk.split(']})')[0] + ']}'
            elif ')})}' in dk:
                dk = dk.split(')})}')[0] + ')}'
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
                    if str(round(time.time()))[:4] in s and len(s.split(':')) == 3:
                        self.flow_data['flow_url'] = s
                        break

        for i,v in enumerate(self.js.split("='")):
            if len(v.split('~')) > 500:
                for code in v.split('~'):

                    if len(code) == 65 and ('+' in code and '-' in code):
                        self.flow_data['turnstile_siteKey'] = code

                    if len(code) in [49, 50] and 'explicit' in code:
                        self.flow_data['onload_token'] = code.split('onload=')[1].split('&')[0]
                        self.flow_data['really_a_key'] = code.split('/')[1]

        self.f_less = int(self.js.split('f=f-')[1].split(',')[0])

        for i,v in enumerate(self.js.split('parseInt(')):
            if '}(' in v[:500]:
                variaba = v.split('}(')[1][:2]
                #print(v)
                self.obf_number = int(v.split('}(' + variaba)[1].split('),')[0].replace('\n', '').strip())

        self.parseInt = self.parseInt_values()
        self.interactive_data = self.intauto_values()

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

                if i == 0 and 'eM[' in v[(len(v) - 30):len(v)]:
                    _v = v[(len(v) - 6):len(v)].split('(')[1].split(')')[0]
                    ReversedObjects.chl_opt_keys['other'].append(self.find_obf_value(_v))

        for i,v in enumerate(self.js.split('65535')):
            #print('PRESICIOOOOOON', v)
            #print('LALLALALALALLALALALALALAL', v[len(v) - 200:len(v)])
            if '255' in v[(len(v) - 50):len(v)] and i in [0, 1]:
                for sym in v[(len(v) - 50):len(v)].split('2'):
                    #print('BROOOOO TJI', sym[:30], '\n')
                    if sym[:2] == '55':
                        #print('CALALALALLALA', sym[:20])
                        p = 2
                        if sym[2:3] == '.' and not sym[4:5].isnumeric():
                            p = 4
                        elif sym[2:3] == '.' and sym[4:5].isnumeric():
                            p = 5
                        ReversedObjects.decrypt_presicion = '2' + sym[:p]

        if self.is_flow_auto:
            for i,v in enumerate(self.js.split(".ch||")):
                if v[(len(v) - 2100):len(v)].count('||') >= 5 and i in [0, 1]:
                    o = v[(len(v) - 2100):len(v)]

                    for lo in o.split('eM'):
                        if lo[:1] == '[' and 'eN[' in lo[15:25] and '(' in lo[38:50]:
                            value = lo.split('][')[1].split('(')[1].split(')')[0]
                            ReversedObjects.chl_opt_keys['what_hello']['fragment'] = self.find_obf_value(value)
                            break

        #print('calala:', ReversedObjects.decrypt_presicion)

        #print(ReversedObjects.chl_opt_keys)

        OrchestrateJS.set_orchestrate_data(self.interactive_data)

        _int_keys_l = list(self.interactive_data.keys())
        _int_values_I = list(self.interactive_data.values())
 
        self.complete_interactive_data(_int_values_I, unk_values)
        #print(self.flow_data)
        #print(ReversedObjects.chl_opt_keys)
        #sys.exit()

#if __name__ == '__main__':
#    c = CF_Solver(
#        'https://nopecha.com/demo/cloudflare',
#        siteKey='0x4AAAAAAAAjq6WYeRDKmebM'
#    )
#    orc = c.cf_orchestrate_js(False)
#    p = OrchestrateJS(orc, auto_mode=False)
#    p.parse_params()
#    print(p.flow_data)
