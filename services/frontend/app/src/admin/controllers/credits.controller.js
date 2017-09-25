module = angular.module("jupiter.admin");
module.controller("CreditsController", CreditsController);

function CreditsController($http, $auth, $error, $location, $url, creditStatuses) {
    var ctrl = this;
    ctrl.data = [];
    ctrl.filterParams = $location.search();
    ctrl.creditStatuses = creditStatuses;

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getCredits = function () {
        ctrl.queryParams = {
            "client__first_name__icontains": ctrl.filterParams.client_name,
            "template__exact": ctrl.filterParams.template,
            "residue__gt": ctrl.filterParams.residue,
            "status__exact": ctrl.filterParams.status,
            "client__exact": ctrl.filterParams.client_id
        };

        var url = $auth.addUrlAuth('/api/credits/');
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

    this.getCreditTemplates = function () {
        ctrl.templates = [];
        $http.get('/api/credits/templates/').then(
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
