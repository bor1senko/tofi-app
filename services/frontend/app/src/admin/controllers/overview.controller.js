module = angular.module("jupiter.admin");
module.controller('OverviewController', OverviewController);


function OverviewController($http, $error, $auth,
                           creditStatuses, depositStatuses, accountStatuses) {
    var ctrl = this;
    ctrl.creditStatuses = creditStatuses;
    ctrl.depositStatuses = depositStatuses;
    ctrl.accountStatuses = accountStatuses;
    ctrl.userStatuses = {
        "True": "Активен",
        "False": "Деактивирован"
    };

    ctrl.statistics = {};
    this.getInfo = function () {
        var url = $auth.addUrlAuth('/api/users/info/');
        ctrl.statistics.users = null;
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.users = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );

        ctrl.statistics.accounts = null;
        url = $auth.addUrlAuth('/api/accounts/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.accounts = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );

        ctrl.statistics.deposits = null;
        url = $auth.addUrlAuth('/api/deposits/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.deposits = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );

        ctrl.statistics.credits = null;
        url = $auth.addUrlAuth('/api/credits/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.credits = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    }
}
