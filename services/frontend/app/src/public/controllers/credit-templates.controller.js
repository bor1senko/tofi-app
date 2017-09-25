module = angular.module("jupiter.public");
module.controller('CreditTemplatesController', CreditTemplatesController);


function CreditTemplatesController($http, $routeParams, $error) {
    var ctrl = this;

    this.getCreditTemplates = function () {
        ctrl.data = [];
        $http.get('/api/credits/templates/').then(
            function success(response) {
                ctrl.data = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.getCreditTemplate = function () {
        ctrl.data = {};
        var url ='/api/credits/templates/' + $routeParams["id"] + '/';
        $http.get(url).then(
            function success(response) {
                ctrl.data = response.data;
                ctrl.errors = null;
            },
            $error.onError
        )
    }
}
