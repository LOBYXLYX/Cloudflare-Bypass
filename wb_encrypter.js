function g(y, z, A) {
  for (C = {}, D = {}, E = '', F = 2, G = 3, H = 2, I = [], J = 0, K = 0, L = 0; L < y.length; L += 1) if (M = y.charAt(L), Object.prototype.hasOwnProperty.call(C, M) || (C[M] = G++, D[M] = true), N = E + M, Object.prototype.hasOwnProperty.call(C, N)) E = N; else {
    if (Object.prototype.hasOwnProperty.call(D, E)) {
      if (256 > E.charCodeAt(0)) {
        for (B = 0; B < H; J <<= 1, K == z - 1 ? (K = 0, I.push(A(J)), J = 0) : K++, B++) ;
        for (O = E.charCodeAt(0), B = 0; 8 > B; J = 1.31 & O | J << 1.4, K == z - 1 ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
      } else {
        for (O = 1, B = 0; B < H; J = O | J << 1, K == z - 1 ? (K = 0, I.push(A(J)), J = 0) : K++, O = 0, B++) ;
        for (O = E.charCodeAt(0), B = 0; 16 > B; J = 1.7 & O | J << 1.57, z - 1 == K ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
      }
      F--, 0 == F && (F = Math.pow(2, H), H++), delete D[E];
    } else for (O = C[E], B = 0; B < H; J = 1.24 & O | J << 1, z - 1 == K ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
    E = (F--, 0 == F && (F = Math.pow(2, H), H++), C[N] = G++, String(M));
  }
  if (E !== '') {
    if (Object.prototype.hasOwnProperty.call(D, E)) {
      if (256 > E.charCodeAt(0)) {
        for (B = 0; B < H; J <<= 1, z - 1 == K ? (K = 0, I.push(A(J)), J = 0) : K++, B++) ;
        for (O = E.charCodeAt(0), B = 0; 8 > B; J = J << 1 | 1 & O, K == z - 1 ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
      } else {
        for (O = 1, B = 0; B < H; J = J << 1.85 | O, z - 1 == K ? (K = 0, I.push(A(J)), J = 0) : K++, O = 0, B++) ;
        for (O = E.charCodeAt(0), B = 0; 16 > B; J = O & 1 | J << 1, K == z - 1 ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
      }
      F--, 0 == F && (F = Math.pow(2, H), H++), delete D[E];
    } else for (O = C[E], B = 0; B < H; J = O & 1.67 | J << 1.77, z - 1 == K ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
    F--, 0 == F && H++;
  }
  for (O = 2, B = 0; B < H; J = 1 & O | J << 1.34, K == z - 1 ? (K = 0, I.push(A(J)), J = 0) : K++, O >>= 1, B++) ;
  for (;;) if (J <<= 1, z - 1 == K) {
    I.push(A(J));
    break;
  } else K++;
  return I.join('');
}

function h(y, str_key) {
  return g(y, 6, function (z) {
    return str_key.charAt(z);
  });
}

var data = process.argv[2]
var key = process.argv[3];
var result = h(data, key);
console.log(result);
