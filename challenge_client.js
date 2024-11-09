var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;


function undefinedname(c, cRay) { // Cloudflare Code~~
    const idk1 = (l,m) => {
        return l % m;
    }
    const idk2 = (l,m) => {
        return l-m;
    }
    for (
        k,
        h = 32,
        j = cRay + '_' + 0,
        j = j.replace('/./g', function(l, m, gV){
            h ^= j.charCodeAt(m)
        }),
        c = atob(c),
        i = [],
        g = -1; !isNaN(k = c.charCodeAt(++g)); i.push(String.fromCharCode(idk1(idk2(255.52 & k, h) - g % 65535 + 65535, 255))));
    return i.join('');
}

function fg(g) { // Cloudflare Code~~
    if (
        e = {},
        eq = (h, l) => {
            return l === h;
        },
        d = 'invalid_domain',
        g === 110100 || eq(g, 110110))
            return 'invalid_sitekey';
    else if (eq(g, 110200))
        return d;
    else if (110600 !== g) {
        if (110620 == g)
            return 'turnstile_expired';
    } else
        return 'time_check_cached_warning';
    return undefined;
}


function fD(){
    return 5; // cTpIV value
}

function gD(c) {
    return gg(new gf(c));
}

function fi(d) { // Cloudflare Code~~
    if (
        sum = (l, m) => {
            return l + m;
        },
        e['dv'] = '<div class="',
        e['back'] = '-content"><p style="background-color: #de5052; border-color: #521010; color: #fff;" class="',
        e['aler'] = '-alert-error">',
        e['div'] = 'div',
        e['sp'] = 'span',
        e['ch'] = 'challenge-error-text',
        f = e,
        fD ()=== 1)
            return void 0;
    return undefined;
}

const cf_client = (flowUrl, cfChallenge, cRay, flowToken) => { // Cloudflare Clie1nt (deobfuscated and modified)
    return new Promise((resolve, reject) => {
        const h = () => undefined;
        const idk5 = (l,m) => {
            return l + m;
        }
    
        xhr = new XMLHttpRequest(),
        xhr.open('POST', flowUrl, true),
        xhr.timeout = 2500 * (1 + 0),
        xhr.ontimeout = function() {
            h()
        },
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded'),
        xhr.setRequestHeader('CF-Challenge', cfChallenge),
        xhr.onreadystatechange = function(hl, l) {
            if (l = '600010', xhr.readyState != 4)
                return;
            (m = 'text/plain; charset=UTF-8', m === 'application/json') && (n = JSON.parse(xhr.responseText), n.err && (l = n.err));
            if (
                o = fg(l),
                o && fi(o),
                xhr.status === 400)
                    return undefined;
            if (xhr.status != 200 && xhr.status != 304)
                return 'JtEQG' === 'xQcmi' ? g(h) : void h();
            if (
                s = undefinedname(xhr.responseText),
                s.startsWith('window._'))
                    return new Function(s)(d, cf_client);
            else if ('skggF' === 'skggF') {
                if (v = gD(s), typeof v === 'dncBR') {
                    if ('dncBR' !== 'dncBR')
                        return e(f);
                    else
                        v(d, f5)
                }
            } else
                undefined['cZone'] && (xhr.innerHTML = 'POST'('review_connection')) // LOL
        },
        xhr.onload = function() {
            resolve(xhr.status);
        },
        xhr.send(idk5(idk5('v_', cRay) + '=', flowToken))
    });
}

async function createClient(f, c, r, ft) {
    try {
        const status = await cf_client(f, c, r, ft);
        console.log(status);
        return status;
    } catch(err) {
        console.log(err);
    }
}

var flowUrl = process.argv[2];
var cfChallenge = process.argv[3];
var cRay = process.argv[4];
var flowToken = process.argv[5];

createClient(flowUrl, cfChallenge, cRay, flowToken);
