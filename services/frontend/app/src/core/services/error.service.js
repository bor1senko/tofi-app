module = angular.module("jupiter.core");
module.service("$error", ErrorService);

function ErrorService($location, $timeout) {
    var self = this;

    this.onSuccess = function (message) {
        self.success = message;
        self.errors = null;
        self.globalHTTPError = null;
        $timeout(self.hideAlert, 3000);
    };

    this.onError = function (response) {
        if (response.status == 400) {
            self.errors = this.prettifyErrors(response.data);
            self.success = null;
            $timeout(self.hideAlert, 3000);
        }
        else {
            self.globalHTTPError = {
                status: response.status,
                message: response.statusText
            };
            $location.path('/error/');
        }
    };

    this.clearErrors = function () {
        self.errors = null;
        self.globalHTTPError = null;
    };

    this.hideAlert = function () {
        self.clearErrors();
        self.success = null;
    };

    this._prettify = function (data) {
        var errors = {};
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                if ($.isArray(data[key])) {
                    errors[key] = data[key][0].toString();
                }
                else if (typeof data[key] == 'object') {
                    errors = $.extend({}, errors, this._prettify(data[key]))
                }
                else {
                    errors[key] = data[key].toString();
                }
            }
        }
        return errors;
    };

    this.prettifyErrors = function (data) {
        if ($.isArray(data)) {
            return {"Ошибка": data[0].toString()}
        }
        else if (typeof data == 'object') {
            return this._prettify(data)
        }
        else {
            return {"Ошибка": data.toString()}
        }
    }

}
