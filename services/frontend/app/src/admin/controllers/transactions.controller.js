module = angular.module("jupiter.admin");
module.controller('TransactionsController', TransactionsController);


function TransactionsController($http, $error, $auth, $location,
                                $url, $scope, $filter, transactionTypes) {
    var ctrl = this;
    ctrl.data = [];
    ctrl.filterParams = $location.search();
    ctrl.transactionTypes = transactionTypes;

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    $scope.toogleStartDatePicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.startDateOpened = !$scope.startDateOpened;
    };

    $scope.toogleEndDatePicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.endDateOpened = !$scope.endDateOpened;
    };

    this.getTransactions = function () {
        if (!ctrl.filterParams.startDate) {
            var previousMonth = new Date();
            previousMonth.setMonth(previousMonth.getMonth() - 1);
            ctrl.filterParams.startDate = previousMonth;
        }

        ctrl.filterParams.startDate = new Date(ctrl.filterParams.startDate);
        ctrl.filterParams.endDate = new Date(ctrl.filterParams.endDate || new Date);

        ctrl.queryParams = {
            "client__first_name__icontains": ctrl.filterParams.client_name,
            "client__exact": ctrl.filterParams.client_id,
            "product__name__istartswith": ctrl.filterParams.product,
            "type__exact": ctrl.filterParams.type,
            "created_on__gt": $filter('date')(ctrl.filterParams.startDate, 'yyyy-MM-dd 00:00'),
            "created_on__lt": $filter('date')(ctrl.filterParams.endDate, 'yyyy-MM-dd 23:59'),
            "ordering": "-created_on"
        };

        var url = $auth.addUrlAuth('/api/transactions/');
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
}
