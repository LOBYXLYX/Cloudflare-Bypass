
const parseUndefined = array => { // parse values that have undefined string
    var modified = {};
    var i = () => undefined;

    Object.entries(JSON.parse(array)).forEach(([key, value]) => {
        if (value === 'undefined') value = i();

        modified[key] = value;
    });
    return JSON.stringify(modified);
}
