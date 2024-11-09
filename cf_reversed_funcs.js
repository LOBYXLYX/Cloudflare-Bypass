

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

function l() {
    var a = 'abcdefghijklmnopqrstuvwxyz0123456789', i = a.length, t;
    do {
        t = "";
        for (var d = 0; d < 5; d++)
            t += a.charAt(Math.floor(Math.random() * i))
    } while (y.widgetMap.has(t));
    return t
};


