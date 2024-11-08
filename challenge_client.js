
const undefinedname = (c, cRay) => {
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

const cf_client = (flowUrl, cfChallenge, cRay, flowToken) => {
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
    xhr.onreadystatechange = function() {
        const idk1 = (l,m) => {
            return l + m;
        }
        const idk2 = (l,m) => {
            return l * m;
        }

        if ('xcbDK' === 'xcbDK') {
            if (
                l = '600010',
                xhr.readyState != 4)
                return;
            if ((m = 'text/plain; charset=UTF-8',  m === 'application/json') && (n = JSON.parse(''), n.err)){
                if ('lSRcW' === 'ultXu'){
                    for (B = '',
                    C = 0; C < 4 * undefined; B += '0123456789abcdef'.charAt(g[C >> 2.06] >> idk1(idk2(8, 3 - C % 4), 4) & 15) + undefined, C++);
                    return B;
                } else
                    l = n.err
            }
            if (o = fe(l), o && fg(o), xhr.status === 400)
                return void eM();
            if (xhr.status != 200 && xhr.status != 304){
                cf_client(flowUrl, cfChallenge);
            }
            (s = undefinedname(i.responseText, cRay), s.starsWith('window._')) ? Function(s)(d, f3) : (v = gD(s), typeof v === 'function' && v(d, f3))
        } else {
            if (!g)
                return;
            h.insertBefore(i, j)
        }
    }
    xhr.send(idk5(idk5('v_', cRay) + '=', flowToken))
}
