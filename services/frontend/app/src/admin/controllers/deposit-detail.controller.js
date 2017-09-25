module = angular.module('jupiter.admin');
module.controller('DepositDetailController', DepositDetailController);


function DepositDetailController($http, $auth, $routeParams, depositStatuses,
                                 accountStatuses, $route, $scope, $error)
{
    var ctrl = this;
    ctrl.deposit = null;
    ctrl.errors = null;
    ctrl.accoiunts = null;
    ctrl.depositStatuses = depositStatuses;
    ctrl.accountStatuses = accountStatuses;
    ctrl.account_id = null;

    ctrl.getData = function() {
        var url ="/api/deposits/" + $routeParams["id"] + "/";
        $http.get($auth.addUrlAuth(url)).then(
            function success(response) {
                ctrl.deposit = response.data;
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

    ctrl.close = function(account_id) {
        var url = "/api/deposits/" + $routeParams["id"] + "/leave_close_claim/";
        $http.patch($auth.addUrlAuth(url), {
            target_account_id: account_id
        }).then(
            function success(response) {
                $route.reload();
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response)
            }
        );
    };

    ctrl.canResolveCreate = function() {
        return ctrl.deposit && $scope.user.isAdmin() && ctrl.deposit.status === 3;
    };

    ctrl.canResolveClose = function() {
        return ctrl.deposit && $scope.user.isAdmin() && ctrl.deposit.status === 4;
    };

    ctrl.resolveCreateClaim = function(value, cause) {
        var method = value ?  "confirm_create_claim" : "reject_create_claim";
        var url = "/api/deposits/" + $routeParams["id"] + "/" + method + "/";
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

    ctrl.resolveCloseClaim = function(value, cause) {
        var method = value ?  "confirm_close_claim" : "reject_close_claim";
        var url = "/api/deposits/" + $routeParams["id"] + "/" + method + "/";
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

    ctrl.pay = function(amount, account_id) {
        var url = "/api/deposits/" + $routeParams["id"] + "/put_money/";
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
}