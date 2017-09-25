module = angular.module('jupiter.admin');
module.controller('CreditDetailController', CreditDetailController);


function CreditDetailController($http, $auth, $routeParams,
                                creditStatuses, accountStatuses,
                                $route, $scope, $error)
{
    var ctrl = this;
    ctrl.credit = null;
    ctrl.errors = null;
    ctrl.accounts = null;
    ctrl.creditStatuses = creditStatuses;
    ctrl.accountStatuses = accountStatuses;

    ctrl.getData = function() {
        var url ="/api/credits/" + $routeParams["id"] + "/";
        $http.get($auth.addUrlAuth(url)).then(
            function success(response) {
                ctrl.credit = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );

        url = "/api/accounts/";
        $http.get($auth.addUrlAuth(url)).then(
            function success(response) {
                ctrl.accounts = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    ctrl.canClose = function() {
        return ctrl.credit &&
               $scope.user.isClient() &&
               (ctrl.credit.status === 2);
    };

    ctrl.close = function() {
        var url = "/api/credits/" + $routeParams["id"] + "/close/";
        $http.patch($auth.addUrlAuth(url), {}).then(
            function success(response) {
                $route.reload();
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    ctrl.pay = function(amount, account_id) {
        var url = "/api/credits/" + $routeParams["id"] + "/make_payment/";
        $http.post($auth.addUrlAuth(url), {
            amount: amount,
            account_id: account_id
        }).then(
            function success() {
                $route.reload();
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    ctrl.canResolve = function() {
        return ctrl.credit && $scope.user.isAdmin() && ctrl.credit.status === 5;
    };

    ctrl.resolveClaim = function(value, cause) {
        var method = value ?  "confirm_create_claim" : "reject_create_claim";
        var url = "/api/credits/" + $routeParams["id"] + "/" + method + "/";
        ctrl.processing = true;
        $http.patch($auth.addUrlAuth(url), {
            cause: cause || ''
        }).then(
            function success(response) {
                ctrl.processing = false;
                $route.reload();
                $error.clearErrors();
            },
            function error(response) {
                ctrl.processing = false;
                $error.onError(response);
            }
        );
    };
}