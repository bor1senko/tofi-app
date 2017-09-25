module = angular.module("jupiter.admin");
module.controller("AccountsController", AccountsController);

function AccountsController($http, $auth, $error, $location, $url,
                            accountStatuses, clientAccountStatuses)
{
    var ctrl = this;
    ctrl.filterParams = $location.search();
    ctrl.accountStatuses = accountStatuses;
    ctrl.clientAccountStatuses = clientAccountStatuses;

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getAccounts = function () {
        ctrl.queryParams = {
            "number__startswith": ctrl.filterParams.number,
            "client__first_name__istartswith": ctrl.filterParams.name,
            "residue__gt": ctrl.filterParams.residue,
            "status__exact": ctrl.filterParams.status
        };

        var url = $auth.addUrlAuth('/api/accounts/');
        for (var key in ctrl.queryParams) {
            if (ctrl.queryParams.hasOwnProperty(key) && ctrl.queryParams[key]) {
                url = $url.query(url, key, ctrl.queryParams[key]);
            }
        }

        ctrl.data = null;
        $http.get(url).then(
            function success(response) {
                ctrl.data = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    ctrl.account_data = {
        account_number: ""
    };

    this.assignAccount = function () {
        var url = $auth.addUrlAuth('/api/accounts/assign/');
        $http.post(url, ctrl.account_data).then(
            function success(response) {
                ctrl.getAccounts();
                $error.onSuccess('Счет успешно добавлен');
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.unassignAccount = function (id) {
        var url = $auth.addUrlAuth('/api/accounts/' + id + '/unassign/');
        $http.post(url, ctrl.account_data).then(
            function success(response) {
                ctrl.getAccounts();
                $error.onSuccess('Счет успешно удален');
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.createRequest = function () {
        var url = $auth.addUrlAuth('/api/accounts/leave_create_claim/');
        $http.post(url, {}).then(
            function success(response) {
                $error.onSuccess(response.data);
                ctrl.getAccounts();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.confirmCreateRequest = function (account) {
        var url = $auth.addUrlAuth('/api/accounts/' + account.id + '/confirm_create_claim/');
        account.processing = true;
        $http.post(url, {}).then(
            function success(response) {
                $error.onSuccess(response.data);
                ctrl.getAccounts();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.rejectCreateRequest = function (account) {
        var url = $auth.addUrlAuth('/api/accounts/' + account.id + '/reject_create_claim/');
        account.processing = true;
        $http.post(url, {}).then(
            function success(response) {
                $error.onSuccess(response.data);
                ctrl.getAccounts();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.closeRequest = function(id) {
        var url = $auth.addUrlAuth('/api/accounts/' + id + '/unassign/');
        $http.post(url, {
            target_account_id: id
        }).then(
            function success(response) {
                ctrl.getAccounts();
                $error.onSuccess(response.data);
            },
            function error(response) {
                ctrl.errors = $error.prettifyErrors(response.data);
                ctrl.success = null;
                $error.onError(response);
            }
        );
    }
}
