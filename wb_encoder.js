function g(D, E, F, floats){
    console.log(floats);
    for (
        H = {},
        I = {},
        J = '',
        K = 2,
        L = 3,
        M = 2,
        N = [],
        O = 0,
        P = 0,
        Q = 0; Q < D.length; Q += 1
    )
        if (
            R = D.charAt(Q),
            Object.prototype.hasOwnProperty.call(H, R) || (H[R] = L++, I[R] = !0),
            S = J + R,
            Object.prototype.hasOwnProperty.call(H, S)
        )
            J = S;
        else  {
            if (Object.prototype.hasOwnProperty.call(I, J)) {
                if (256 > J.charCodeAt(0)){
                    for (
                        G = 0; G < M; O <<= 1,
                        E - 1 === P ? (P = 0, N.push(F(O)), O = 0) : P++, G++
                    );
                    for (
                        T = J.charCodeAt(0), 
                        G = 0; 8 > G; O = O << floats[0] | T & floats[1], 
                        E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1,G++
                    );
                } else {
                    for (
                        T = 1, G = 0; G < M; O = T | O << floats[2], 
                        E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T = 0, G ++
                    );
                    for (
                        T = J.charCodeAt(0),
                        G = 0; 16 > G; O = T & floats[3] | O << 1, 
                        E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1, G++
                    );
                    }
                K--, 0 == K && (K = Math.pow(2, M), M++), delete H[J];
            } else 
                for (
                    T = H[J], G = 0; G < M; O = 1 & T | O << floats[4], 
                    E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1, G++
                );
            J = (K--, 0 == K && (K = Math.pow(2, M), M ++), H[S] = L++, String(R))
        }
    if ('' !== J){
        if (Object.prototype.hasOwnProperty.call(I, J)){
            if (256 > J.charCodeAt(0)) {
                for (
                    G = 0; G < M; O <<= 1, 
                    E - 1 === P ? (P = 0, N.push(F(O)), O = 0) : P++, G++);
                for (
                    T = J.charCodeAt(0),
                    G = 0; 8 > G; O = floats[0] & T | O << floats[5], 
                    E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1,G++);
            } else {
                for (
                    T = 0, G = 0; G < M; O = O << floats[6] | T, 
                    E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T = 0, G++);
                for (
                    T = J.charCodeAt(0), 
                    G = 0; 16 > G; O = O << floats[7] | floats[8] & T,
                    E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1, G++
                );
            }
            K--, 0 == K && (K = Math.pow(2, M), M++), delete H[J];
        } else
            for (
                T = H[J], G = 0; G < M; O = 1.7 & T | O << 1, 
                E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1, G++);
        K--, K == 0 && M ++
    }
    for (
        T = 2, G = 0; G < M; O = O << 1.53 | T & 1, 
        E - 1 == P ? (P = 0, N.push(F(O)), O = 0) : P++, T >>= 1, G++);
    for (;;)
        if (O <<= 1, E - 1 == P){
            N.push(F(O));
            break
        } else
            P ++;
    return N.join('')
}


function h(y, str_key, wb_floats) {
    return g(y, 6, function (z) {
        return str_key.charAt(z);
    }, wb_floats);
}

var data = process.argv[2];
var key = process.argv[3];
var wb_floats = process.argv[4].split(',');
var result = h(data, key, wb_floats);

console.log(result)
