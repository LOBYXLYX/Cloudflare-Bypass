class BlueTooth {
    constructor() {
        this.onadvertisementreceived = null;
    }
}
class ClipBoard {
    constructor() {}
}
class NetworkInformation {
    constructor() {
        this.downlink = 1.45;
        this.downlinkMax = (1e311);
        this.effectiveType = '4g';
        this.onchange = null;
        this.ontypechange = null;
        this.rtt = 0;
        this.saveData = false;
        this.type = 'wifi'
    }
}
class ContactsManager {
    constructor() {}
}
class CredentialsContainer {
    constructor() {}
}
class DevicePosture {
    constructor() {
        this.onchange = null;
        this.type = 'continuous';
    }
}
class Geolocation {
    constructor() {}
}
class WSGLLanguageFeatures {
    constructor() {
        this.size = 0;
    }
}
class GPU {
    constructor() {
        this.wgslLanguageFeatures = new WSGLLanguageFeatures();
    }
}
class Ink {
    constructor() {}
}
class Keyboard {
    constructor() {}
}
class LocksManager {
    constructor() {}
}
class NavigatorManagedData {
    constructor() {
        this.onmanagedconfigurationchange = null;
    }
}
class MediaCapabilities {
    constructor() {}
}
class MediaDevices {
    constructor() {}
}
class MediaSession {
    constructor() {
        this.metadata = null;
        this.playbackState = 'none';
    }
}
class MimeTypeArray {
    constructor() {
        this.length = 0;
    }
}
class ML {
    constructor() {}
}
class Permissions {
    constructor() {}
}
class PluginArray {
    constructor() {
        this.length = 0;
    }
}
class Presentation {
    constructor() {
        this.defaultRequest = null;
        this.receiver = null;
    }
}
class Scheduling {
    constructor() {}
}
class ServiceWorkerContainer {
    constructor() {
        this.controller = null;
        this.oncontrollerchange = null;
        this.onmessage = null;
        this.onmessageerror = null;
    }
}
class StorageManager {
    constructor() {
        this.onquotachange = null;
    }
}
class StorageBucketManager {
    constructor() {}
}
class USB {
    constructor() {
        this.onconnect = null;
        this.ondisconnect = null;
    }
}
class UserActivation {
    constructor() {
        this.hasBeenActive = false;
        this.isActive = false;
    }
}
class NavigatorUAData {
    constructor() {
        this.brands = [
            {brand: 'Not-A.Brand', version: '99'},
            {brand: 'Chromium', version: '124'}
        ];
        this.mobile = true;
        this.platform = 'Android';
    }
}
class DOMRect {
    constructor() {
        this.bottom = 0;
        this.height = 0;
        this.left = 0;
        this.right = 0;
        this.top = 0;
        this.width = 0;
        this.x = 0;
        this.y = 0;
    }
}
class VirtualKeyboard {
    constructor() {
        this.boundingRect = new DOMRect();
        this.ongeometrychange = null;
        this.overlaysContent = false;
    }
}
class XRSystem {
    constructor() {
        this.ondevicechange = null;
    }
}
class WakeLock {
    constructor() {}
}
class DeprecatedStorageQuota {
    constructor() {}
}
class NavigationHistoryEntry {
    constructor() {
        this.id = '03df9dc8-4c2b-4148-917c-e3508f3a739e';
        this.index = 0;
        this.key = 'db62fa24-b3ed-47a4-bd63-d97a4f7f2c72';
        this.ondispose = null;
        this.sameDocument = true;
        this.url = '';
    }
}
class Navigation {
    constructor() {
        this.canGoBack = false;
        this.canGoForward = false;
        this.currentEntry = new NavigationHistoryEntry();
        this.onnavigate = null;
        this.oncurrententrychange = null;
        this.onnavigateerror = null;
        this.onnavigatesuccess = null;
        this.transition = null;
    }
}
window._navigatorIDTest = crypto.randomUUID()
window.mockPerformance = function(entryType, initiator, name) {
    return {
        initiatorType: initiator,
        name: name,
        entryType: entryType,
        encodedBodySize: Math.floor(Math.random() * (9000 - 300 + 1)) + 100,
        requestStart: Math.random() * (200 - 100) + 50,
        responseStart: Math.random() * (300 - 400) + 70,
        responseEnd: Math.random() * (450 - 700) + 100,
        duration: Math.random() * (200 - 300) + 20,
        startTime: Math.random() * (200 - 300) + 20,
        navigationId: window._navigatorIDTest
    }
}
window.matchMedia = function (query) {
    const width = window.innerWidth || 1024;
    const height = window.innerHeight || 768;

    const matches = evaluateMediaQuery(query, { width, height });

    let listener = null;

    return {
        matches,
        media: query,
        addEventListener: (event, callback) => {
            if (event === "change") listener = callback;
        },
        removeEventListener: () => {
            listener = null;
        },
        dispatchChange: () => {
            if (listener) {
                const newMatches = evaluateMediaQuery(query, {
                    width: window.innerWidth,
                    height: window.innerHeight,
                });
                listener({ matches: newMatches, media: query });
            }
        },
    };
    function evaluateMediaQuery(query, dimensions) {
        const { width } = dimensions;

        if (query.includes("max-width")) {
            const maxWidth = parseInt(query.match(/max-width:\s*(\d+)px/)[1], 10);
            return width <= maxWidth;
        }
        if (query.includes("min-width")) {
            const minWidth = parseInt(query.match(/min-width:\s*(\d+)px/)[1], 10);
            return width >= minWidth;
        }
        return false;
    }
}
    
window.HTMLCanvasElement.prototype.getContext = function () {
    return {
        fillRect: function() {},
        clearRect: function(){},
        getImageData: function(x, y, w, h) {
            return  {
                data: new Array(w*h*4)
            };
        },
        putImageData: function() {},
        createImageData: function(){ return []},
        setTransform: function(){},
        drawImage: function(){},
        save: function(){},
        fillText: function(){},
        restore: function(){},
        beginPath: function(){},
        moveTo: function(){},
        lineTo: function(){},
        closePath: function(){},
        stroke: function(){},
        translate: function(){},
        scale: function(){},
        rotate: function(){},
        arc: function(){},
        fill: function(){},
        measureText: function(){
            return { width: 0 };
        },
        transform: function(){},
        rect: function(){},
        clip: function(){},
    };
}
window.HTMLCanvasElement.prototype.toDataURL = function () {
    return "";
}
window.chrome = {
    'app': {},
    'csi': function(){},
    'loadTimes': function(){}
}
window.navigation = new Navigation()
window.simulation_getClientRects = function () {
  const simulatedRects = [
    {
      x: 10,
      y: 20,
      width: 100,
      height: 50,
      top: 20,
      left: 10,
      bottom: 70,
      right: 110,
    },
    {
      x: 30,
      y: 50,
      width: 150,
      height: 80,
      top: 50,
      left: 30,
      bottom: 130,
      right: 180,
    },
  ];
  return {
    length: simulatedRects.length,
    item(index) {
      return simulatedRects[index] || null;
    },
    ...simulatedRects,
  };
};

const clientNavigator = userAgent => {
    // navigator client simulation
    var language = 'es-CO';
    var languages_list = ['es-CO', 'es-US', 'es-419', 'es'];

    window.clientInformation = {
        appCodeName: userAgent.split('/')[0],
        appName: 'Netscape',
        appVersion: userAgent.split('Mozilla/')[1],
        bluetooth: new BlueTooth(),
        clipboard: new ClipBoard(),
        connection: new NetworkInformation(),
        contacts: new ContactsManager(),
        cookieEnabled: true,
        credentials: new CredentialsContainer(),
        deviceMemory: (2 << Math.floor(Math.random() * 6)),
        devicePosture: new DevicePosture(),
        doNotTrack: null,
        geolocation: new Geolocation(),
        gpu: new GPU(),
        hardwareConcurrency: 8,
        ink: new Ink(),
        keyboard: new Keyboard(),
        language: language,
        languages: languages_list,
        locks: new LocksManager(),
        managed: new NavigatorManagedData(),
        maxTouchPoints: 5,
        mediaCapabilities: new MediaCapabilities(),
        mediaDevices: new MediaDevices(),
        mediaSession: new MediaSession(),
        mimeTypes: new MimeTypeArray(),
        ml: new ML(),
        onLine: true,
        pdfViewerEnabled: false,
        permissions: new Permissions(),
        platform: 'Linux x86_64',
        plugins: new PluginArray(),
        presentation: new Presentation(),
        product: 'Gecko',
        productSub: '20030107',
        scheduling: new Scheduling(),
        serviceWorker: new ServiceWorkerContainer(),
        storage: new StorageManager(),
        storageBuckets: new StorageBucketManager(),
        usb: new USB(),
        userActivation: new UserActivation(),
        userAgent: userAgent,
        userAgentData: new NavigatorUAData(),
        vendor: 'Google Inc.',
        vendorSub: '',
        virtualKeyboard: new VirtualKeyboard(),
        wakeLock: new WakeLock(),
        webdriver: false,
        webkitPersistentStorage: new DeprecatedStorageQuota(),
        webkitTemporaryStorage: new DeprecatedStorageQuota(),
        xr: new XRSystem()
    }
    return window
}
