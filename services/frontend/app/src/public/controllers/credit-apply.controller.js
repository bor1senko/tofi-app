module = angular.module("jupiter.public");
module.controller("CreditApplicationController", CreditApplicationController);


function CreditApplicationController(
    $http, $routeParams, ensuringMethods, moneyDestinations, $error, $auth, $location, accountStatuses
) {
    var ctrl = this;
    ctrl.ensuringMethods = ensuringMethods;
    ctrl.moneyDestinations = moneyDestinations;
    ctrl.accountStatuses = accountStatuses;

    ctrl.template = null;
    ctrl.account_id = null;
    ctrl.accounts = null;
    ctrl.duration = null;
    ctrl.amount = null;
    ctrl.ensuringMethod = "0"; // fine by default
    ctrl.moneyDestination = "0"; // into account by default

    this.getData = function () {
        var url ='/api/credits/templates/' + $routeParams["id"] + '/';
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

    this.apply = function() {
        if (!ctrl.template) {
            return;
        }
        var method = ctrl.template.issue_online ? 'open_online' : 'leave_create_claim';
        var url = '/api/credits/' + method + '/';
        ctrl.processing = true;
        $http.post($auth.addUrlAuth(url), {
            account_id: ctrl.account_id,
            template_id: ctrl.template.id,
            duration: ctrl.duration,
            amount: ctrl.amount,
            ensuring_method: ctrl.ensuringMethod,
            money_destination: ctrl.moneyDestination
        }).then(
            function success() {
                ctrl.processing = false;
                $location.path("/credits/");
                $error.clearErrors();
            },
            function error(response) {
                ctrl.processing = false;
                $error.onError(response);
            }
        );
    };
}
