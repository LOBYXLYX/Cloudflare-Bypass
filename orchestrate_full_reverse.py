import sys
import types
import json
import time
import typing
import random
import string
import execjs
from javascript import require, globalThis


jsdom = require('jsdom')
vm = require('vm')
node_atob = require('atob')
jsdom_worker = require('jsdom-worker')
node_fetch = require('node-fetch').default

PATH = 'cloudflare-data/orchestrate.json'
reversed_funcs = execjs.compile(open('cf_reversed_funcs.js', 'r').read())
reverse_utility = execjs.compile(open('_reverse_utility.js', 'r').read())


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
    decrypt_values: dict[str, typing.Any] = {}
    initialized_onload: bool = False
    decrypt_presicion: float = 255
    onload_challenge = None

class VM_Automation:
    def __init__(self, domain, userAgent, cf_html=False, html_code=None):
        self.domain = domain
        self.userAgent = userAgent
        self.resource_loader = jsdom.ResourceLoader({'userAgent': self.userAgent})
        self.dom_context = None
        self.ov1_contentType = 'application/x-www-form-urlencoded'
        self.html_code = html_code

        virtualConsole = jsdom.VirtualConsole()
        virtualConsole.on("error", lambda: ());

        self.window = jsdom.JSDOM(self._cf_create_html(cf_html, html_code), {
            'url': self.domain,
            'referrer': self.domain + '/',
            'contentType': 'text/html',
            'includeNodeLocations': True,
            'pretendToBeVisual': True,
            'storageQuota': 10000000,
            'runScripts': 'dangerously',
            #'virtualConsole': virtualConsole,
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
        self.window.innerHeight = 65
        self.window.innerWidth = 300
        self.window.outerHeight = 987
        self.window.outerWidth = 524

        self.window.origin = 'https://challenges.cloudflare.com'
        self.window.originAgentCluster = False
        self.window.orientation = 0
        self.window.isSecureContext = True
        self.window.fetch = node_fetch
        self.window.atob = node_atob
        self.window.Worker = globalThis.Worker
        globalThis.FileReader = self.window.window.FileReader

        self.window.URL = vm.Script('URL').runInThisContext()
        self.window.stuffed_html = open('cloudflare-data/stuffed.html', 'r').read()

        # cloueflare turnstile onload
        vm.Script(open('_window.js', 'r').read()).runInContext(self.window)
        vm.Script('''
        window.lt = function(e) {
            return e > 0 && e < 36e4;
        }
        window.It = function (e) {
            var r =
                arguments.length > 1 && arguments[1] !== void 0 ? arguments[1] : 3;
            return e.length > r ? e.substring(0, r) : e;
        };
        window.vr = function(e) {
            if (!e) return "-";
            var r = function (n, o) {
                if (!n || n.tagName === "BODY") return o;
                for (var c = 1, u = n.previousElementSibling; u; )
                    u.tagName === n.tagName && c++, (u = u.previousElementSibling);
                var g = window.It(n.tagName.toLowerCase()),
                    h = "".concat(g, "[").concat(c, "]");
                return r(n.parentNode, "/".concat(h).concat(o));
            };
            return r(e, "");
        }
        window.mr = function(e, r, n) {
            for (
                var o = "",
                    c = 0,
                    u = document.createNodeIterator(
                        e,
                        NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
                        {
                            acceptNode: function (I) {
                                return c > r || o.length > n
                                    ? NodeFilter.FILTER_REJECT
                                    : NodeFilter.FILTER_ACCEPT;
                            },
                        }
                    ),
                    g;
                (g = u.nextNode()) !== null && o.length < n;

            ) {
                if (g.nodeType === Node.ELEMENT_NODE) {
                    var h = g;
                    o += "".concat(window.It(h.tagName.toLowerCase()));
                    for (var l = 0; l < h.attributes.length; l++) {
                        var p = h.attributes[l];
                        o += "_".concat(window.It(p.name, 2));
                    }
                    o += ">";
                } else g.nodeType === Node.TEXT_NODE && (o += "-t");
                var E = g.parentNode;
                for (c = 0; E !== e && E !== null; ) c++, (E = E.parentNode);
            }
            return o.substring(0, n);
        }
        window.gr = function(e) {
            if (typeof e != "string")
                throw new Error(
                    "djb2: expected string, got ".concat(
                        typeof e == "undefined" ? "undefined" : F(e)
                    )
                );
            for (var r = 5381, n = 0; n < e.length; n++) {
                var o = e.charCodeAt(n);
                r = (r * 33) ^ o;
            }
            return r >>> 0;
        }

        window.mockPerformance('navigation', 'navigation', '_domain')
        '''.replace('_domain', self.domain)).runInContext(self.window)

        vm.Script('clientNavigator("_ua")'.replace('_ua', self.userAgent)).runInContext(self.window)

    def _cf_create_html(self, html, code) -> str:
        if html:
            if code is not None:
                return code
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
        elif func_name == 'errorl':
            return code.split('//errl')[1].split('//lolerr')[0]
        elif func_name == 'unknown_decryp':
            return code.split('//unk_decryp')[1].split('//decryp_fin')[0]

    def send_ov1_request(
        self, 
        flowUrl, 
        flowToken, 
        cfChallenge, 
        cfRay, 
        referrer, 
        decrypter
    ) -> str:
        print('cloudflare challenge URL:\033[36m', flowUrl, '\033[0m')
        print('request payload:', f'v_{cfRay}={flowToken[:100]}....')
        print(len(flowToken))

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
        #print(result['encrypted'][:100])

        if not result['success']:
            raise TypeError(f'Cloudflare Challenge Failed ({result["encrypted"]})')
        window_decrypted = decrypter(result['encrypted'], cfRay)

        if 'challenges' in flowUrl:
            open('cloudflare-data/decrypted.js', 'w').write(window_decrypted)
        #print('decrypted:', window_decrypted[:90])
        #sys.exit()
        return window_decrypted

    @staticmethod
    def analyze_obf(
        number, 
        f_less, 
        obf_code, 
        obf_number, 
        parseint_gen, 
        parentesis, 
        _return_c=False, 
        split_type='~'
    ) -> str:
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
        result = vm.Script('b(Number(NUMBER))'.replace('NUMBER', str(number)).split(')')[0] + '))').runInThisContext()
        print(number, result)
        return result

    def reverse_website_identifier(self, _return_c=False) -> dict[typing.Union[int, str], typing.Any]:
        vm.Script(self.get_reversed_func('iden')).runInContext(self.window)
        codee = '''
        function ffEge(D, E, F, G) {
            //if (E === null || E === void 0)
            //    return G;

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

    def onload_postMessage(self, code, data: dict[str, typing.Any]):
        vm.Script(code).runInContext(self.window)
        vm.Script('window.parent.postMessage(__, "*")'.replace('__', json.dumps(data))).runInContext(self.window)

    def emulate_decryption(self, response, binteractive, obf_functions, **kwargs):
        self.window._cf_chl_opt = ReversedObjects.cf_chl_opt
        self.window.TextEncoder = vm.Script('TextEncoder').runInThisContext()

        vm.Script(VM_Automation.analyze_obf(number=None, **kwargs, _return_c=True, split_type='~')).runInContext(self.window)
        vm.Script('''
        eM = window
        eN = window.document
        console.log(window._cf_chl_opt)
        var gF = (number) => b(number);'''
        ).runInContext(self.window)

        for function in obf_functions:
            vm.Script(function).runInContext(self.window)
            print('success')
        vm.Script(
        '''
        function fC(c,d,e,hY,f,m,n,o,g,h,i,j,k){if(hY = (number) => b(number),console.log(c, d, e),f={'AUoUw':function(l){return l()},'QzoIe':function(l,m){return l(m)},'XUZXq':function(l,m,n,o){return l(m,n,o)},'FneDN':function(l,m){return m*l},'UQRfq':function(l,m){return l+m},'MFNPN':hY(835),'yizRw':function(l,m){return m===l},'KBLXR':function(l,m){return l+m},'QOwBS':hY(870),'YHfVL':hY(570),'LVAwF':hY(603),'yqXGN':hY(1075),'riSlD':hY(633),'olEzU':hY(175),'YzGfF':function(l,m){return m!=l},'QMyNP':function(l,m){return m===l},'PCTSq':function(l,m){return l===m},'Qdgwt':hY(972),'KucHW':function(l,m,n){return l(m,n)},'akrwS':hY(518),'RkTNJ':hY(724),'eLheY':hY(1016),'TzyBl':hY(844)},e=e||0,f[hY(153)](fF,hY(956))||e>=3){if(hY(518)===f[hY(697)])return void eM[hY(609)]();else m=f[hY(270)](k),n=l[hY(273)](f[hY(153)](m,m)),n(n)&&(n=0),f[hY(933)](o,m,n+1,1),o=f[hY(763)](1e3,s[hY(1236)][hY(400)](2.32<<n,32)),v[hY(1244)](function(hZ){hZ=hY,m[hZ(513)][hZ(434)]()},o)}if(g=![],h=function(i0){if(i0=hY,i0(435)===f[i0(1256)])return f[i0(722)].cK&&g[i0(722)].cK[i0(1096)](h)!==-1;else{if(g)return;g=!![],eM[i0(1244)](function(i1){i1=i0,fB++,f[i1(933)](fC,c,d,f[i1(184)](e,1))},250*(e+1))}},i=new eM[(hY(292))](),!i)return;j=hY(665),i[hY(350)](j,c,!![]),i[hY(217)]=f[hY(763)](5e3,f[hY(184)](1,e)),i[hY(1267)]=function(i2){i2=hY,f[i2(270)](h)},i[hY(1101)](hY(1055),hY(913)),i[hY(1101)](f[hY(1268)],eM[hY(722)].cH),i[hY(1101)](f[hY(408)],fB),i[hY(1005)]=function(i3,C,m,n,o,s,v,x,F,G){if(i3=hY,i3(633)!==f[i3(418)])C=i+i3(612),!j[i3(209)][i3(1026)](i3(431))&&(f[i3(271)](k[i3(513)][i3(766)],i3(1003))||l[i3(931)]&&!m())&&(C+=i3(1137)),n[i3(993)]=C;else{if(m=f[i3(387)],f[i3(266)](i[i3(1248)],4))return;(n=this[i3(978)](i3(1132)),n===i3(460))&&(o=JSON[i3(1150)](i[i3(890)]),o[i3(279)]&&(m=o[i3(279)]));if(s=f[i3(153)](fN,m),s){if(i3(1001)!==i3(1001))throw this.h[this.h[60^this.g][3]^f[i3(508)](this.h[this.g^60.08][1][i3(1149)](this.h[60.29^this.g][0]++)-232,256)&255.48^153^this.g];else fP(s)}if(i[i3(182)]===400)return f[i3(582)](i3(720),i3(575))?void 0:void eM[i3(609)]();if(i[i3(182)]!=200&&i[i3(182)]!=304)return void h();if(v=eO(i[i3(890)]),v[i3(377)](i3(386)))new eM[(i3(286))](v)(d,fC);else if(x=fi(v),f[i3(707)](typeof x,i3(1062))){if(f[i3(588)]===f[i3(588)])f[i3(1247)](x,d,fC);else return F=l(i3(1189)),m=n[i3(1200)](f[i3(706)]),o[i3(289)]=f[i3(1036)],s[i3(948)][i3(1181)]=i3(505),G=v[i3(1200)](i3(444)),G[i3(1098)]=f[i3(1160)],G[i3(323)]=F,G[i3(1081)][i3(618)](f[i3(473)]),x[i3(616)](G),B()[i3(616)](C),G}}},k=eP[hY(395)](JSON[hY(483)](d))[hY(1130)]('+',f[hY(185)]),i[hY(1120)](f[hY(508)]('v_',eM[hY(722)][hY(624)])+'='+k)}
        B = notdecrypted("resp")
        console.log('kakakak', B)
        B(chl_inter, fC)
        '''.replace('resp', response).replace('chl_inter', binteractive)).runInContext(self.window)
        sys.exit()

    @staticmethod
    def encrypt_flow_data(
        data, 
        turnkey, 
        enc_code, 
        obf_v, 
        operators, 
        split_type='~', 
        **kwargs
    ) -> str:
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

    def decrypt_response(response, func, **kwargs):
        vm.Script(VM_Automation.analyze_obf(number=None, **kwargs, _return_c=True)).runInThisContext()
        vm.Script('var gF = (number) => b(Number(number))').runInThisContext()
        vm.Script(func).runInThisContext()
        result = vm.Script(f'decrypt_response("{response}")').runInThisContext()
        return result

    def evaluate(
        self,
        code: str, 
        decryptedChl: str, 
        flow_auto: bool = False,
        previous_data: dict[str, typing.Any] = None
    ) -> dict[str, typing.Any]:
        #sendRequest = lambda arg1, arg2: print(arg1, arg2)


        self.window.decryptedChl = decryptedChl
        self.window._cf_chl_opt = ReversedObjects.cf_chl_opt
        #self.window.sendRequest = sendRequest

        if flow_auto:
            shd = code.split(".mode === 'closed'")[0]
            shdow = shd[len(shd) - 40:len(shd)].split('window._cf_chl_opt.')[1]
            ReversedObjects.chl_opt_keys['what_hello']['fragment'] = shdow

        self.window._o_k = ReversedObjects.chl_opt_keys['what_hello']
        self.window._o_s = ReversedObjects.chl_opt_keys['_setTimeout']
        self.window.vm_script = vm
        
        _0xL = self.window._o_k['fragment']

        # why jsdom doesnt have Blob, URL and TextEncoder?
        #self.window.Blob = vm.Script('Blob').runInThisContext()
        #self.window.URL = vm.Script('URL').runInThisContext()
        self.window.TextEncoder = vm.Script('TextEncoder').runInThisContext()
        self.window._performance = vm.Script('performance').runInThisContext()

        def _parse_window_eval():
            nonlocal code

            if flow_auto:
                if "contentWindow.screen.orientation,'so.'" in code:
                    t = code.split(".screen.orientation,'so.',")[1].split('var d={};d=')[1].split('(')[0]
                    code = code.replace(t, 'ffEge')
                    code = code.replace(",c=ffEge(b,a.contentWindow.screen.orientation,'so.',c)", '')
                    unknown_func = code.split(",window,'',d),")[1].split('(')[0]
                else:
                    unknown_func = 'UNKNOWN_1209'

                func_err = code.split('var errorInfoObject = window.')[1].split('(')[0]
                err_req = code.split(func_err)[1].split('window.')[1].split('(')[0]

                if 'getClientRects' in code:
                    unk_decryp = code.split('.getClientRects())')[1].split('.length')[1].split('();return}')[1].split('(JSON')[0]
                else:
                    unk_decryp = 'UNKNOWN_1210'

                if 'ht.atrs' in code:
                    _d = code.split("['ht.atrs']")[0]
                    bludthis = _d[len(_d) - 15:len(_d)].split('_chl_opt.')[1]
                else:
                    bludthis = 'UNKNOWN_1211'

                additional_code = '''
                var _unknown_f = function(h, i) {
                    gw = '_cco_coma'.split(':');
                    gx = gw.includes.bind(gw)
                    for (i = Object.keys(i), m = 0; m < l.length; m++) {
                        if (n = l[m], 'f' === n && (n = 'N'), h[n]) {
                            for (
                                o < 0; o < i[l[m]].length; -1 === h[n].indexOf(i[l[m]][o]) && (gx(i[l[m]][0]) || h[n].push('0.' + i[l[m]][o])), o++);
                        } else
                            h[n] = i[l[m]].map(function (s) {
                                return '0.' + s;
                            })
                        }
                }

                var _unknown_req = function(){} // simulation
                var nr = 3, ar = 500, ir = 500;

                var wrapper = document.createElement("div");
                wrapper.innerHTML = `
                <input type="hidden" name="cf-turnstile-response" id="cf-chl-widget-q0kml_response">
                <input type="hidden" name="cf_challenge_response" id="cf-chl-widget-q0kml_legacy_response"
                `;

                window._cf_chl_opt.blud_is_this = {
                    "w.iW": window.innerWidth,
                    "ht.atrs": ["lang", "dir"],
                    "pi": {
                        "xp": window.vr(wrapper).substring(0, ir),
                        "pfp": window.mr(document, nr, ar),
                        "sL": 4,
                        "ssL": 2,
                        "mL": document.getElementsByTagName("meta").length,
                        "t": window.gr(document.title),
                        "tL": document.getElementsByTagName('*').length,
                        "lH": "_thesiteurl_?__cf_chl_rt_tk=_tk_chl_token",
                        "sR": true
                    }
                }
        
                document.body.innerHTML = ''
                console.log(window._performance.getEntries())
                '''.replace('_unknown_f', unknown_func).replace('_unknown_req', err_req).replace('blud_is_this', bludthis).replace('_thesiteurl_', ReversedObjects.cf_chl_opt['chlApiUrl']).replace('_tk_chl_token', ReversedObjects.cf_chl_opt['_rttk']).replace('q0kml', ReversedObjects.cf_chl_opt['chlApiWidgetId']).replace('_cco_coma', ReversedObjects.chl_opt_keys['what_hello']['cco_coma'])

                additional_code += self.get_reversed_func('errorl').replace('errorl', func_err)
                additional_code += self.get_reversed_func('unknown_decryp').replace('unknown_decryp', unk_decryp)

                vm.Script(additional_code).runInContext(self.window)


            obj, prop = code.split("('ur-handler")[0].split('(!window.')[1].split('.')

            vm.Script('''
            window._o0 = {_p0: null};

            window._o0._p0 = function(c){
                return window._cf_chl_opt.cK && window._cf_chl_opt.cK.indexOf(c) !== -1
            }
            '''.replace('_o0', obj).replace('_p0', prop)).runInContext(self.window)

        shadow_html = open('cloudflare-data/turnstile_html.html', 'r').read()
        _parse_window_eval()

        vm.Script('''
        //console.log(window._cf_chl_opt)
        window.sendRequest = function(arg1, arg2){console.log(arg1, arg2)}

        window.Worker = class {
            constructor(blobURL) {
                this.messageListeners = [];
                this.errorListeners = [];
                this.terminated = false;
                try {
                    const blobContent = this._getBlobContent(blobURL);
                    this.Self = {
                        postMessage: (message) => {
                            setImmediate(() => {
                                this.messageListeners.forEach((listener) => listener({ data: message }));
                            });
                        },
                        onmessage: null,
                        onerror: null,
                        terminate: () => {
                            this.terminated = true;
                        }
                    };
                } catch (error) {
                    this.errorListeners.forEach((listener) => listener(error));
                }
            }
            _getBlobContent(blobURL) {
                const base64Content = blobURL.split(',')[1];
                return Buffer.from(base64Content, 'base64').toString('utf-8');
            }
    
            postMessage(message) {
                if (this.terminated) return;
        
                setImmediate(() => {
                    if (this.Self === undefined) return;
                    if (typeof this.Self.onmessage === 'function') {
                        try {
                            this.Self.onmessage({ data: message });
                        } catch (error) {
                            this.errorListeners.forEach((listener) => listener(error));
                        }
                    }
                    new Promise((resolve, reject) => {
                        var context = window.vm_script.createContext(this.Self);
                        resolve(window.vm_script.runInContext(message, context));
                    });
                });
            }
            terminate() {
                this.terminated = true;
            }
        };
        var contain = window.document.createElement('div')
        //window.document.body.appendChild(contain);
        
        var _shadow = contain.attachShadow({mode: 'closed'});
        _shadow.innerHTML = `_sha_html`

        window._cf_chl_opt[window._o_k['fragment']] = _shadow

        Object.entries(_prev_d).forEach(([k, v]) => {
            window._cf_chl_opt[k] = v
        })

        '''.replace('_sha_html', shadow_html).replace('__htmlc', self.html_code).replace('_prev_d', previous_data)).runInContext(self.window)
        vm.Script(self.reverse_website_identifier(True)).runInContext(self.window)

        _getclientrects_code = "'pr'+f);console.log('lala', g);g.getClientRects = window.simulation_getClientRects;"

        c = code.replace('arguments[0]', 'JSON.parse(window.decryptedChl)').replace('arguments[1]', 'window.sendRequest').replace(f'window._cf_chl_opt.{_0xL}.appendChild', 'window.document.body.appendChild').replace(f'window._cf_chl_opt.{_0xL}.removeChild', 'window.document.body.removeChild').replace('g.getClientRects()', 'true').replace('window.performance', 'window._performance')
        open('cloudflare-data/ccc.js', 'w').write(c)

        vm.Script(c).runInContext(self.window)
        if flow_auto:
            vm.Script('''
            Object.entries(JSON.parse(_prev_data)).forEach(([k, v]) => {
                if ((_cf_chl_ctx[k] === undefined || isNaN(_cf_chl_ctx[k]) || _cf_chl_ctx[k] === null) && Object.prototype.hasOwnProperty.call(_cf_chl_ctx, k)) {
                    _cf_chl_ctx[k] = v
                }
            })
            '''.replace('_prev_data', json.dumps(previous_data))).runInContext(self.window)
            vm.Script('console.log(_cf_chl_ctx)').runInContext(self.window)
            vm.Script('window.decryptedChl = _cf_chl_ctx').runInContext(self.window)

        result = json.loads(vm.Script('JSON.stringify(_cf_chl_ctx)').runInContext(self.window))
        vm.Script('window.Worker = undefined;').runInContext(self.window) # avoid  SyntaxError: Identifier 'Worker' has already been declarede
        return result

    def evaluate_captcha(self, code: str, decryptedChl: str):
        _0xL = self.window._o_k['fragment']
        self.window.Worker = globalThis.Worker

        clientx = str(random.randint(25, 45))
        clienty = str(random.randint(40, 55))

        screenx = str(random.randint(49, 52))
        screeny = str(random.randint(350, 366))

        obj = code.split('var handle = window.')[1].split('.')[0]

        handlec = code.split(f'if(!window.{obj}.')[1].split("('ur-handler')")[0]
        fo_func = code.split('new Error().stack,')[1].split(f'window.{obj}.')[1].split('();')[0]

        rd1 = code.split('var onMessage = function(e) {')[1].split('window.')[1]
        fd, fd2 = rd1.split('(function() {')[0].split('.')

        all_code = '''
        window.sendRequest = function(arg1, arg2){console.log(arg1, arg2)}

        var _handthise = function(d) {
            return window._cf_chl_opt.cK && window._cf_chl_opt.cK.indexOf(d) !== -1
        }
        var _fo = function() {
            if (d = 'challenge_running', false) {
                return;
            }
        }

        window._obj0_ = {}
        window._obj0_._handlerr = _handthise
        window._obj0_.fO_fO = _fo
        window._fded_ = {}
        window._fded_.ffunc = function(c){c()};
        '''.replace('_obj0_', obj).replace('_handlerr', handlec).replace('fO_fO', fo_func).replace('_fded_', fd).replace('ffunc', fd2)

        vm.Script(all_code).runInContext(self.window)

        click_code = '''
        clickEvent = new window.MouseEvent("click", {
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: _cx,
            clientY: _cy,
            screenX: _sx,
            screenY: _sy
        });
        handle.dispatchEvent(clickEvent);'''.replace('_cx', clientx).replace('_cy', clienty).replace('_sx', screenx).replace('_sy', screeny).replace('\n', '').strip().replace(' ', '').replace('newwindow.MouseEvent', 'new window.MouseEvent').replace(';', ';\n')
        print('clicking cloudflare captcha\033[33m X:', clientx, 'Y:', clienty, '\033[0m')

        for i,v in enumerate(code.split(f'window.{obj}')):
            if v[:1] == '.' and '();' in v[:10]:
                code = code.replace(f'window.{obj}{v.split("(")[0]}();', '')

        c = code.replace('arguments[0]', 'window.decryptedChl').replace('arguments[1]', 'window.sendRequest').replace('performance', '_performance').replace(f'window._cf_chl_opt.{_0xL}.appendChild', 'window.document.body.appendChild').replace(f'window._cf_chl_opt.{_0xL}.removeChild', 'window.document.body.removeChild').replace("String(e['y']);", "String(e['y']);console.log(eventData);").replace("var handle =", "document.body.innerHTML = `<!DOCTYPE html><html><body><button id='myButton'>Click me</button></body></html>`\nvar handle = document.getElementById('myButton');").replace("if (chlctx['GCPy6'] === 0) {", click_code+"\nif (chlctx['GCPy6'] === 0) {").replace('killwindow.Workers', 'killwindow_Workers').replace("URL.createObjectURL(new Blob([`onmessage=function(e){e.isTrusted&&''===e.origin&&null===e.source&&eval(e.data)}`], {type: 'text/javascript'}));", "URL.createObjectURL(new Blob([`onmessage=function(e){eval(e.data)}`], {type: 'text/javascript'}));").replace('setTimeout(after_clicked, 250);', 'after_clicked();')

        vm.Script(c).runInContext(self.window)

        vm.Script('''
        Object.entries(JSON.parse(_prev_data)).forEach(([k, v]) => {
            if (_cf_chl_ctx[k] === undefined && Object.prototype.hasOwnProperty.call(_cf_chl_ctx, k)) {
                _cf_chl_ctx[k] = v
            }
        })

        _cf_chl_ctx.ghvEF2 = 'MggmBxpUUhE9LBQkAlVHTgQEDQBLBmlcC04EXwZMDRRFRA8FVFREXmVvVHY7'
        '''.replace('_prev_data', json.dumps(decryptedChl))).runInContext(self.window)

        result = vm.Script('''
        console.log(_cf_chl_ctx)
        ''').runInContext(self.window)
        result = vm.Script('JSON.stringify(_cf_chl_ctx)').runInContext(self.window)
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

    def decrypter_response(self, response, cf_ray):
        for i,v in enumerate(self.js.split('isNaN')):
            if '=32' in v[len(v) - 4000:len(v)] and '/./g' in v[len(v) - 3000:len(v)]:
                o = v[len(v) - len(v):len(v)].split(',')
            elif '=32' in v[len(v) - 500:len(v)] and '/./g' in v[len(v) - 300:len(v)]:
                o = v[len(v) - 800:len(v)].split(',')

        def _dl(i, o):
            for _ in range(10, 35):
                if '(/./g' in o[i + _]:
                    return True
            return False

        for i,p in enumerate(o):
            t = ['c', 'f']
            for ted in t:
                if (p[:2].isalpha() or (p[:1].isalpha() and p[1:2].isnumeric())) and f'=function({ted}' in p[2:14]:
                    func = self.js.split(f'{p[:2]}=function(')[1]
        
                    if "('')}}," in func[:4600]:
                        func = func.split("('')}},")[0] + "('')}}"
                    elif "('')}," in func[:4600]:
                        func = func.split("('')},")[0] + "('')}"

                    l = f'decrypt_response=function(' + func
                    v = l[:100].split('{for(')[1].split(',')[0].split('=')[1]
    
                    func = l.replace(v, 'gF').replace('eM[', 'window[')
                    break

                if p == f'function({ted}' and _dl(i, o):
                    a = o[(i - 1 if f'function({ted}' in p else i + 1)]
    
                    g = f'{a},{p}'
                    if 'function' in p:
                        a =p
                        p = f'function({ted}'

                    func = self.js.split(g)[1].split("('')})")[0] + "('')}"
    
                    l = f'decrypt_response={a}' + func
                    v = l[:100].split('{for(')[1].split(',')[0].split('=')[1]
    
                    func = l.replace(v, 'gF').replace('eM[', 'window[')
                    break

        for i,v in enumerate(func.split('window')):
            if "'_'" in v[:50]:
                d = v[:50]
    
                if ")]+'_'" in d:
                    s = d.split("+'_")[0]
                elif ")],'_'" in d:
                    s = d.split(",'_")[0]

                func = func.replace(f'window{s}', f'"{cf_ray}"')
            if ')](' in v[:15] and '=[]' in v[:25]:
                u = v.split('](')[0] + ']'
                func = func.replace(f'window{u}', 'atob')
            
        result = VM_Automation.decrypt_response(
            response,
            func,
            f_less=self.f_less,
            obf_code=self.parse_js_storaged_code(),
            obf_number=self.obf_number,
            parseint_gen=self.parseInt,
            parentesis=self.double_parentesis
        )
        return result

    def not_window_decrypted(self, response) -> list[str]:
        lett = ['x', 's', 'o', 'v', 'n', 'C', 'D', 'B']
        func_names = []
        funcs = []

        open('cloudflare-data/laputa.js', 'w').write(self.js)

        fr = ''

        for i,v in enumerate(self.js.split('200')):
            if "'v_'" in v[:1000] and "'='" in v[:1000] and '304' in v[:500]:
                for p in v.split('?new eM'):
                    fr = p.split('(JSON[')[0]

        for i,v in enumerate(fr.split(')](')):
            if v[:1].isalpha() and v[1:3] == ')(' and v[:1] in lett:
                o = v[:1]
                d = v.split(')(')[1].split(',')[0]

        _types = [f',{o}),', f'({o}),']

        for t in _types:
            for i,v in enumerate(fr.split(t)):
                if v[len(v) - 2:len(v)].isalpha() and i == 0:
                    w = v[len(v) - 2:len(v)]

        for i,v in enumerate(self.js.split(f'function {w}(')):
            if 'new' in v[:100]:
                z = v.split('}function')[0]

                funcs.append(f'function notdecrypted(' + z + '}')

        for w in z.split('('):
            if w[len(w) - 2:len(w)][:1].isalpha() and ('{return ' in w or 'new ' in w):
                func_names.append(w[len(w) - 2:len(w)])

            if w[:1].isalpha() and w[2:6] == ',new':
                func_names.append(w[:2])

        for func in func_names:
            for i,v in enumerate(self.js.split(f'function {func}(')):
                if len(v[:20].split(',')) >= 3:
                    ready = f'function {func}(' + v.split('}function')[0]

                    if not func.count('this.') > 15:
                        ready += '}'

                    funcs.append(ready)

        for func in funcs:
            if func.count('this.') > 15:
                for e in func.split(']='):
                    if e[:2].isalpha() or (e[:1].isalpha() and e[1:2].isnumeric()):
                        l = e[:2]
                        print(l)

                        for i,v in enumerate(self.js.split(f'function {l}(')):
                            _fun = f'function {l}(' + v.split('}function')[0] + '}'
                            if len(_fun[:30].split(',')) >= 2 or '){' in _fun[:5]:
                                funcs.append(_fun)

                        for i,v in enumerate(self.js.split(f'{l}=')):
                            if '(0,eval)' in v[:20]:
                                ev = v[:25].split('),')[0] + ')'

                                bv = ev.split('eval)(')[1].split('(')[0]
                                ev = f'var {l}=' + ev.replace(bv, 'gF')

                                if ev.count('(') == 4:
                                    ev += ')'
                                funcs.insert(0, ev)

                            if 'atob(' in v[:10]:
                                av = v[:25].split('),')[0] + ')'
                                ov = av.split('atob(')[1].split('(')[0]

                                av = f'var {l}=' + av.replace(ov, 'gF')

                                if av.count('(') == 4:
                                    av += ')'

                                funcs.insert(0, av)

                for r in func.split('[0,'):
                    if r[:2].isalpha() or (r[:1].isalpha() and r[1:2].isnumeric()) and r[2:3] == ',':
                        n = r[:2]

                        for i,v in enumerate(self.js.split(f'function {n}(')):
                            _fun2 = f'function {n}(' + v.split('}function')[0] + '}'

                            if len(_fun2[:30].split(',')) >= 2:
                                funcs.append(_fun2)

                        for i,v in enumerate(self.js.split(f'{n}=')):
                            if '(0,eval)' in v[:20]:
                                ev = v[:25].split('),')[0] + ')'

                                bv = ev.split('eval)(')[1].split('(')[0]
                                ev = f'var {n}=' + ev.replace(bv, 'gF')

                                if ev.count('(') == 4:
                                    ev += ')'

                                funcs.insert(0, ev)

                            if 'atob(' in v[:10]:
                                av = v[:25].split('),')[0] + ')'

                                ov = av.split('atob(')[1].split('(')[0]
                                av = f'var {n}=' + av.replace(ov, 'gF')
                                if av.count('(') == 4:
                                    av += ')'

                                funcs.insert(0, av)


                break

        for i,v in enumerate(self.js.split('127')):
            if '=0,0' in v and '255' in v and ('f.g' in v or 'e.g' in v):
                pk = v.split('}function ')

        for z in pk:
            r = z[:2]

            for i,v in enumerate(self.js.split(f'function {r}(')):
                v = v.split('}function ')[1]

                if 'f.h' in v and '127' in v and '255' and '=0,0' in v and 'while(' in v[(len(v) - 30):len(v)]:
                    print('JOJOJO', v)
                    funcs.insert(0, f'function ' + v + '}')

        for i,v in enumerate(self.js.split(']=String[')):
            if '256>' in v[len(v) - 50:len(v)]:
                t = v[len(v) - 6:len(v)].split('[')[0].split(';')[1]
                print('Lslal', t)
                funcs.insert(0, f'var {t}=[]')

        for i,v in enumerate(self.js.split("NaN,'','',0,[]")):
            if 'this.' in v[(len(v) - 150):len(v)]:
                gk = v[(len(v) - 500):len(v)].split('}function ')

        for l in gk:
            s = l[:2]

            for i,v in enumerate(self.js.split(f'function {s}(')):
                v = v.split('}function ')[1]

                if v.count('this.') > 5 and "NaN,'','',0," in v:
                    print('OMG', v)
                    funcs.insert(0, f'function ' + v + '}')

        #sys.exit()

        _new_funcs = []

        for func in funcs:
            if not func.startswith('var '):
                g = func[:70]

                if '){for(' in g:
                    v = g.split('){for(')[1]
                elif '){' in g:
                    v = g.split('){')[1]
                elif '){if(' in g:
                    v = g.split('){if(')[1]
                elif '){return ' in g:
                    v = g.split('){return ')[1]

                elif '){j=(' in g:
                    v = g.split('){j=(')[1]
            
                v = v.split(',')[0]
        
                if 'if(' in v:
                    v = v.split('if(')[1]
                elif 'return ' in v:
                    v = v.split('return ')[1]
                elif 'j=(' in v:
                    v = v.split('j=(')[1]

                b = v.split('=')[0]
                nfunc = func.replace(v, f'{b} = (number) => b(number)')

                if not nfunc in _new_funcs and ('(' not in v and ')' not in v):
                    _new_funcs.append(nfunc.replace('}}()}', '}}'))
                elif 'new' in func and len(func) < 150:
                    _new_funcs.append(func)
            else:
                _new_funcs.append(func)

        print('\n\n\n')
        for new in _new_funcs:
            print(new)


        result = VM_Automation.emulate_decryption(
            response,
            _new_funcs,
            f_less=self.f_less,
            obf_code=self.parse_js_storaged_code(),
            obf_number=self.obf_number,
            parseint_gen=self.parseInt,
            parentesis=self.double_parentesis
        )

    def execute_decrypter(self, vm, response, base_interactive, parsed_functions):
        result = vm.emulate_decryption(
            response,
            base_interactive,
            parsed_functions,
            f_less=self.f_less,
            obf_code=self.parse_js_storaged_code(),
            obf_number=self.obf_number,
            parseint_gen=self.parseInt,
            parentesis=self.double_parentesis
        )
        

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
            if ",d={'" in v[(len(v) - 2210):(len(v) - 800)] and v.count('function') > 10 and '=String[' in v[(len(v) - 35):len(v)]:
                #print(v[(len(v) - 1570):len(v)])
                #print(v[(len(v) - 1570):len(v)].split(f',d=' + '{'))
                spli1 = v[(len(v) - 2210):len(v)].split(f',d=' + '{')[1]
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
                'cK': [],
                'chlApiLoopFeedbackEnabled': False,
                'chlApiMode': 'managed',
                'chlApiRefreshExpired': 'never',
                'chlApiRefreshTimeout': 'never',
                'chlApiRetry': 'never',
                'cType': 'chl_api_m'
            })
        else:
            if 'eventData' in code and 'handle.addEventListener' in code:
                return window_data

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

            blud_v1 = round(float(mybro_v1.split('(')[1].split(')')[0]))
            blud_v2 = round(float(mybro_v2.split('(')[1].split(')')[0]))

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

                    if len(code) in [363, 364] and ('/' in code and '+' in code):
                        ReversedObjects.decrypt_values['string'] = code

                    if code.startswith('_cf_chl_opt;') and code.count(';') in [15, 17]:
                        ReversedObjects.chl_opt_keys['what_hello']['cco_coma'] = code

        self.f_less = int(self.js.split('f=f-')[1].split(',')[0])

        for i,v in enumerate(self.js.split('parseInt(')):
            if '}}(' in v[:450]:
                variaba = v.split('}(')[1][:2]
                # why round(float()) ans not int() beacause this numbers.... 104e3 900e7 804
                self.obf_number = round(float(v.split('}(' + variaba)[1].split('),')[0].replace('\n', '').strip()))
                break

        self.parseInt = self.parseInt_values()
        self.interactive_data = self.intauto_values()

        # unknown array (super obfuscated)
        unk_values = []
        if ReversedObjects.unknown_array is None:
            #print(i, v)
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
        #ReversedObjects.decrypt_presicion = '255'

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
