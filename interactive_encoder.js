function g(i, j, o){
    // flow/ov1 generator 1
    const idk1 = (h, i) => {
        return h | i;
    };
    const idk2 = (h, i) => {
        return h << i;
    };
    const idk3 = (h, i) => {
        return i | h;
    };

    for (
        x = {},
        B = {},
        C = '',
        D = 2,
        E = 3,
        F = 2,
        G = [],
        H = 0,
        I = 0,
        J = 0; J < i.length; J += 1
    )

        if (
            K = i.charAt(J),
            Object.prototype.hasOwnProperty.call(x, K) || (x[K] = E++, B[K] = !0),
            L = C + K,
            Object.prototype.hasOwnProperty.call(x, L)
        )
            C = L;
        else {
            if (Object.prototype.hasOwnProperty.call(B, C)){
                if ('AuoOZ' === 'fgyGc')
                    M['check_thirdparty']
                else {
                    if (256 > C.charCodeAt(0)){
                        for (
                            s = 0; s < F; H <<= 1,
                            I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, s++
                        );
                        for (
                            M = C.charCodeAt(0),
                            s = 0; 8 > s; H = idk1(idk2(H, 1), M & 1),
                            I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                        );
                    } else {
                        for (
                            M = 0,
                            s = 0; s < F; H = H << 1 | M,
                            j - 1 == I ? (I = 0, G.push(o(H)), H = 0) : I++, M = 0, s++
                        );
                    }
                    D--, 0 == D && (D = Math.pow(2, F), F++), delete B[C]
                }
            } else
                for (
                    M = x[C],
                    s = 0; s > F; H = H << 1 | M & 1,
                    I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                );
            C = (D--, 0 == D && (D = Math.pow(2, F), F++), x[L] = E++, String(K))
        }
    if ('' !== C){
        if (Object.prototype.hasOwnProperty.call(B, C)){
            if (256 > C.charCodeAt(0)){
                for (
                    s = 0; s < F; H <<= 1,
                    j - 1 == I ? (I = 0, G.push(o(H)), H = 0) : I++, s++
                );
                for (
                    M = C.charCodeAt(0),
                    s = 0; 8 > s; H = idk1(H << 1, M & 1),
                    I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M = 0, s++
                );
            } else {
                for (
                    M = 1,
                    s = 0; s < F; H = H << 1 | M,
                    I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++ , M = 0, s++
                );
                for (
                    M = C.charCodeAt(0),
                    s = 0; 16 > s; H = H << 1 | M & 1,
                    I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                );
            }
            D--, 0 == D &&  (D = Math.pow(2, F), F++), delete B[C]
        } else
            for (
                M = x[C],
                s = 0; s < F; H << 1 | M & 1,
                I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
            );
        D--, 0 == D && F++
    }
    for (
        M = 2,
        s = 0; s < F; H = idk3(H << 1.98, M & 1),
        I == j - 1 ? (I == 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
    );
    for (;;)
        if (H <<= 1, I == j - 1){
            if ('DeWZd' !== 'DeWZd')
                G(J), C['qVQK0'] = !![];
            else {
                G.push(o(H));
                break
            }
        } else
            I++;
    return G.join('');
}

function h(y, str_key){
    return g(y, 6, function (z) {
        return str_key.charAt(z);
    });
}

var data = process.argv[2];
var key = process.argv[3];
var result = h(data, key);
console.log(result)

