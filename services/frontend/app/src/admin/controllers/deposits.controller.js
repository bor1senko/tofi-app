module = angular.module("jupiter.admin");
module.controller("DepositsController", DepositsController);

function DepositsController($http, $auth, $error, $location, $url, depositStatuses) {
    var ctrl = this;
    ctrl.data = [];
    ctrl.filterParams = $location.search();
    ctrl.depositStatuses = depositStatuses;

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getDeposits = function () {
        ctrl.queryParams = {
            "client__first_name__icontains": ctrl.filterParams.client_name,
            "amount__gt": ctrl.filterParams.amount,
            "template__exact": ctrl.filterParams.template,
            "status__exact": ctrl.filterParams.status,
            "client__exact": ctrl.filterParams.client_id
        };

        var url = $auth.addUrlAuth('/api/deposits/');
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

    this.getDepositTemplates = function () {
        ctrl.templates = [];
        $http.get('/api/deposits/templates/').then(
            function success(response) {
                ctrl.templates = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };
}
