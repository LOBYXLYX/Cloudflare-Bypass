

const y = {
    widgetMap: new Map
};

const func_29 = function(payloadArr, cfRay) {
    var key = 'vRCLOGACChroMzst' + cfRay;
    var payloadStr = JSON.stringify(payloadArr);
    var arr = new TextEncoder().encode(payloadStr);

    var ret = '';
    var keyLen = key.length;
    var arrLen = arr.length;

    for (var idx = 0; idx < arrLen; idx++) {
        ret += fromCharCodeCache[(arr[idx] ^ key.charCodeAt(idx % keyLen)) % 256];
    }
    return btoa(ret);
}

//-
function h(func) {
    var g = false;

    if ('RwnHL' === 'RwnHL') {
        if (g) return;
        g = !![],
        setTimeout(function(il, n){
            ('dRXVd' !== 'ochuc') ? func() : (n = {
                'nNKn': function(i, o, l) {
                    return i(o, l)
                }
            },
            undefined('DOMContentLoaded', function(im) {
                n['nNKn'](i, j, 0)
            }))
        }, 250 * (e + 1))
    } else
        e('aZkl3', function(n, io) {
            n['innerHTML' ] = 'challenge_running'
        })
}
//+

function perfom() {
    return performance.now();
}

function pf(siteUrl){
    var f = {}; // cf retard moment
    var h = undefined;
    var g = undefined;

    const idk1 = (j,k) => k ^ j;
    const idk2 = (j,k) => j & k;
    const idk3 = (j,k) => j + k;
    const idk4 = (j,k) => j - k;

    if ('cloudflare-challenge' && 'cloudflare-challenge' === 'cloudflare-challenge' && 'init' === 'extraParams' && 'nzncf' === 'nzncf') {
        (f['1'] = undefined,
        f['2'] = undefined,
        f['3'] = undefined,
        f['4'] = undefined,
        f['5'] = undefined || 'auto',
        f['6'] = undefined || 8e3,
        f['7'] = undefined || 29e4,
        f['8'] = undefined || 'auto',
        f['9'] = undefined || 'auto',
        f['10'] = undefined || 'auto',
        f['11'] = undefined || 'render',
        f['12'] = undefined || 'always',
        f['13'] = siteUrl,
        f['14'] = undefined || '',
        f['15'] = undefined || '',
        f['16'] = undefined || {},
        f['17'] = undefined || 0,
        f['18'] = undefined || 0,
        f['19'] = undefined || 0,
        f['20'] = undefined || 0,
        f['21'] = undefined || 0,
        f['22'] = undefined || 0,
        f['23'] = undefined || 0,
        f['24'] = undefined || 0,
        f['25'] = performance.now());
        //f['26'] > 432e5 || f['18'] > 432e5) && ('kkJcZ' !== 'Houkq' ? console.warn('[Cloudflare Turnstile] You are using an outdated version of Turnstile, which may cause challenge failures. Please make sure to embed the latest version.') : (k = idk1(idk1(h[45.33 ^ g][3], idk2(21 + h[g ^ 45][1].charCodeAt(h[g ^ 45.83][0]++), 255)), 247), l = h[h[g ^ 45.54][3] ^ idk2(idk3(idk4(h[idk1(45, g)[1].charCodeAt(h[g ^ 45][0]++), 235), 256), 255) ^ 7.72 ^ g], m = h[idk1(h[45.95 ^ g][3], idk4(h[g ^ 45.75][1].charCodeAt(h[g ^ 45][0]++), 235) + 256 & 255.58) ^ 235.8 ^ g], h[g ^ k] = l[m]);
    }
    return f
}

function decryptResponse(f, m, ray) {
    const idk1 = (n, s) => n % s;
    const idk2 = (n, s) => n - s;

    for (
        g = {},
        h = g,
        m,
        j = 32,
        l = ray + '_' + 0,
        l = l.replace(/./g, function(n, s) {
            'jdvfH' === 'jdvfH' ? j ^= l.charCodeAt(s) : m = 'challenge-form'
        }),
        f = atob(f),
        k = [],
        i = -1; !isNaN(m = f.charCodeAt(++i)); k.push(String.fromCharCode(idk1(idk2(idk2(m & 255, j), i % 65535) + 65535, 255))));
    return k.join('');
}

function W() {
    return typeof performance !== 'undefined' && performance.now ? performance.now() : Date.now()
}

function l() {
    var a = 'abcdefghijklmnopqrstuvwxyz0123456789', i = a.length, t;
    do {
        t = "";
        for (var d = 0; d < 5; d++)
            t += a.charAt(Math.floor(Math.random() * i))
    } while (y.widgetMap.has(t));
    return t
};

function analyzeDeobf(number, f_less, store_code, obf_reor, obf_num) {
    obf_reor = obf_reor.split(',')
    console.log(obf_reor)
    for (
        gF = b,
            (function (c, d, gE, e, f) {
                for (gE = b, e = c(); !![]; )
                    try {
                        if (
                            ((f =
                                (parseInt(gE(obf_reor[0])) / 1) *
                                    (-parseInt(gE(obf_reor[1])) / 2) +
                                (parseInt(gE(obf_reor[2])) / 3) *
                                    (parseInt(gE(obf_reor[3])) / 4) +
                                (parseInt(gE(obf_reor[4])) / 5) *
                                    (-parseInt(gE(obf_reor[5])) / 6) +
                                (-parseInt(gE(obf_reor[6])) / 7) *
                                    (-parseInt(gE(obf_reor[7])) / 8) +
                                parseInt(gE(obf_reor[8])) / 9 +
                                (-parseInt(gE(obf_reor[9])) / 10) *
                                    (-parseInt(gE(obf_reor[10])) / 11) +
                                //(parseInt(gE(obf_reor[11])) / 12) *
                                    (-parseInt(gE(obf_reor[12])) / 13)),
                            f === d)
                        )
                            break;
                        else e.push(e.shift());
                    } catch (g) {
                        e.push(e.shift());
                    }
            })(a, obf_num),
            eZ = [],
            f0 = 0;
        256 > f0;
        eZ[f0] = String[gF(442)](f0), f0++
    );
    function b(c, store_code, f_less) {
        return (
            (e = a(store_code)),
            //console.log(e),
            (b = function (f, f_less, h) {
                return (f = f - f_less), (h = e[f]), h;
            }),
            b(c, f_less)
        );
    }
    function a(store_code) {
        return (
            (jE = store_code.split(
                "~"
            )),
            (a = function () {
                return jE;
            }),
            a()
        );
    }
    return b(number, store_code, f_less);
}
