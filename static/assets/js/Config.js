'use strict';
var Config = (function(){
    const HOST = 'http://localhost';
    const PORT = '5000';
    const VERSION = 'api/v1'
    const URL = `${HOST}:${PORT}`;
    const AUTH_URL = `${HOST}:${PORT}/${VERSION}/auth`;
    const PUBLIC_URL = `${HOST}:${PORT}/${VERSION}`;
    return{
        URL: URL,
        AUTH_URL: AUTH_URL,
        PUBLIC_URL: PUBLIC_URL,
    };
})();
