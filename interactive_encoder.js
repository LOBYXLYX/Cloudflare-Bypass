function g(i, j, o, enc){
    const idk1 = (h, i) => {
        return h | i;
    }
    const idk2 = (h, i) => {
        return h << i;
    }
    const idk3 = (h, i) => {
        return i & h;
    }
    const idk4 = (h, i) => {
        return i | h;
    }

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
            if (Object.prototype.hasOwnProperty.call(B, C)) {
                if (256 > C.charCodeAt(0)) {
                    for (
                        s = 0; s < F; H <<= 1, 
                        I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, s++
                    );
                    for (
                        M = C.charCodeAt(0),
                        s = 0; 8 > s; H = H << 1 | 1 & M,
                        I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                    );
                } else {
                    for (
                        M = 1,
                        s = 0; s < F; H = M | H << enc[0],
                        I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M = 0, s++
                    );
                    for (
                        M = C.charCodeAt(0),
                        s = 0; 16 > s; H = H << enc[1] | M & 1,
                        j - 1 == I ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                    );
                }
                D--, 0 == D && (D = Math.pow(2, F), F++), delete B[C];
            } else
                for (
                    M = x[C],
                    s = 0; s < F; H = idk1(idk2(H, 1), idk3(M, 1)),
                    j - 1 == I ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                );
            C = (D --, 0 == D && (D = Math.pow(2, F), F++), x[L] = E++, String(K))
        }
    if (C !== ''){
        if (Object.prototype.hasOwnProperty.call(B, C)) {
            if ('naOqb' === 'naOqb') {
                if (256 > C.charCodeAt(0)) {
                    for (
                        s = 0; s < F; H <<= 1,
                        I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I ++, s++
                    );
                    for (
                        M = C.charCodeAt(0),
                        s = 0; 8 > s; H = M & 1 | H << 1,
                        I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                    );
                } else {
                    for (
                        M = 1,
                        s = 0; s < F; H = H << enc[2]| M,
                        j - 1 == I ? (I = 0, G.push(o(H)), H = 0) : I++, M = 0, s++
                    );
                    for (
                        M = C.charCodeAt(0),
                        s = 0; 16 > s; H = H << 1 | enc[3] & M,
                        I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I++, M >>= 1, s++
                    );
                }
                D--, 0 == D & (D = Math.pow(2, F), F++), delete B[C];
            } else
                undefined = undefined // cf code Lol
        } else
            for (
                M = x[C],
                s = 0; s < F; H = H << enc[4] | M & 1,
                I == j - 1 ? (I = 0, G.push(o(H)), H = 0) : I ++, M >>= 1, s++
            );
        D --, 0 == D && F ++
    }
    for (
        M = 0,
        s = 0; s < F; H = idk4(H << 1.52, idk3(M, 1)),
        j - 1 == I ? (I = 0, G.push(o(h)), H = 0) : I++, M >>= 1, s++
    );
    for (;;)
        if (H <<= 1, I == j - 1) {
            G.push(o(H));
            break
        } else
            I++;
    return G.join('')
}

function h(y, str_key, enc){
    return g(y, 6, function (z) {
        return str_key.charAt(z);
    }, enc);
}

var data = process.argv[2];
var key = process.argv[3];
var enc_floats = process.argv[4].split(',');
var result = h(data, key, enc_floats);
console.log(result)
