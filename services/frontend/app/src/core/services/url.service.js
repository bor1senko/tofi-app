module = angular.module("jupiter.core");
module.service("$url", UrlService);


function UrlService() {

    this.query = function(url, key, value) {
        if (url.search('\\?') === -1) { url += '?'; }
        else { url += '&'}
        return url + key + '=' + value;
    }
}
