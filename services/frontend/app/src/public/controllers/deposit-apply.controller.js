module = angular.module('jupiter.public');
module.controller('DepositApplicationController', DepositApplicationController);


function DepositApplicationController(
    $http, $routeParams, $auth, $error, $location, currencies, accountStatuses
) {
    var ctrl = this;

    ctrl.template = null;
    ctrl.errors = null;
    ctrl.accounts = null;
    ctrl.currencies = currencies;
    ctrl.accountStatuses = accountStatuses;

    ctrl.account_id = null;
    ctrl.currency = null;
    ctrl.amount = null;
    ctrl.plan_index = null;

    ctrl.getData = function() {
        var url ='/api/deposits/templates/' + $routeParams["id"] + '/';
        $http.get($auth.addUrlAuth(url)).then(
            function success(response) {
                ctrl.template = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
        $http.get($auth.addUrlAuth("/api/accounts/")).then(
            function success(response) {
                ctrl.accounts = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    ctrl.apply = function() {
        if (!ctrl.template) {
            return;
        }
        var plan = ctrl.template.currency[ctrl.currency].percentage[ctrl.plan_index];
        ctrl.processing = true;
        $http.post($auth.addUrlAuth('/api/deposits/leave_create_claim/'), {
            percentage: plan.percentage,
            account_id: ctrl.account_id,
            currency: ctrl.currency,
            template_id: ctrl.template.id,
            amount: ctrl.amount,
            duration: plan.term
        }).then(
            function success() {
                ctrl.processing = false;
                $location.path('/deposits/');
                $error.clearErrors();
            },
            function error(response) {
                ctrl.processing = false;
                $error.onError(response);
            }
        );
    }
}
