

y = {
    widgetMap: new Map
};


function l() {
    var a = 'abcdefghijklmnopqrstuvwxyz0123456789', i = a.length, t;
    do {
        t = "";
        for (var d = 0; d < 5; d++)
            t += a.charAt(Math.floor(Math.random() * i))
    } while (y.widgetMap.has(t));
    return t
};
