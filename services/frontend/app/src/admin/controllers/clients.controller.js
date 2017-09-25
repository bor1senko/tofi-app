module = angular.module("jupiter.admin");
module.controller('ClientsController', ClientsController);


function ClientsController($http, $error, $auth, $routeParams,
                           $scope, $filter, $location, $url, $route,
                           creditStatuses, depositStatuses, transactionTypes)
{
    var ctrl = this;
    ctrl.creditStatuses = creditStatuses;
    ctrl.depositStatuses = depositStatuses;
    ctrl.transactionTypes = transactionTypes;

    $scope.toggleBirthDatePicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.birthDatePickerOpened = !$scope.birthDatePickerOpened;
    };

    $scope.togglePassportExpiresPicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.passportExpiresPickerOpened = !$scope.passportExpiresPickerOpened;
    };

    ctrl.filterParams = $location.search();
    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getClients = function () {
        ctrl.data = [];

        ctrl.queryParams = {
            "first_name__istartswith": ctrl.filterParams.name,
            "profile__identification_number__icontains": ctrl.filterParams.in,
            "profile__passport_number__istartswith": ctrl.filterParams.pn,
            "is_active": ctrl.filterParams.state
        };

        var url = $auth.addUrlAuth('/api/users/');
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

    this.getClient = function () {
        ctrl.data = [];
        $http.get($auth.addUrlAuth('/api/users/' + $routeParams['id'] + '/')).then(
            function success(response) {
                ctrl.data = response.data;
                $error.clearErrors();

                $('.tab-link').click(function (e) {
                    e.preventDefault();
                    $(this).tab('show')
                });
            },
            function error(response) {
                $error.onError(response);

                $('.tab-link').click(function (e) {
                    e.preventDefault();
                    $(this).tab('show')
                });
            }
        );
    };

    this.activateClient = function(client) {
        client.processing = true;
        $http.get($auth.addUrlAuth('/api/users/' + client.id + '/activate/')).then(
            function success(response) {
                ctrl.getClients();
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        )
    };

    this.deactivateClient = function(client) {
        client.processing = true;
        $http.get($auth.addUrlAuth('/api/users/' + client.id + '/deactivate/')).then(
            function success(response) {
                ctrl.getClients();
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        )
    };

    this.updateClient = function() {
        var birthDate = ctrl.data.profile.birth_date;
        ctrl.data.profile.birth_date = $filter('date')(birthDate, 'yyyy-MM-dd');

        var passportExpires = ctrl.data.profile.passport_expires;
        ctrl.data.profile.passport_expires = $filter('date')(passportExpires, 'yyyy-MM-dd');

        $http.patch($auth.addUrlAuth('/api/users/' +  $routeParams['id'] + '/'), ctrl.data).then(
            function success(response) {
                ctrl.getClient();
                $error.onSuccess('Профайл успешно изменен');
            },
            function error(response) {
                $error.onError(response);
            }
        )
    };

    this.getClientStatistics = function () {
        $http.get($auth.addUrlAuth('/api/users/' +  $routeParams['id'] + '/statistics/')).then(
            function success(response) {
                ctrl.statistics = response.data;
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        )
    };

    ctrl.changePasswordData = {};
    this.changePassword = function() {
        var url = $auth.addUrlAuth('/api/users/' +  $routeParams['id'] + '/change_password/');
        $http.post(url, ctrl.changePasswordData).then(
            function success(response) {
                ctrl.getClient();
                $error.onSuccess('Пароль успешно изменен');
            },
            function error(response) {
                $error.onError(response);
            }
        )
    };

    ctrl.credentials = {};
    this.createAdmin = function () {
        $http.post($auth.addUrlAuth('/api/users/create_admin/'), ctrl.credentials).then(
            function success(response) {
                $route.reload();
                $error.onSuccess('Администратор успешно создан');
            },
            function error(response) {
                $error.onError(response);
            }
        )
    };

    this.deleteUser = function (id) {
        $http.delete($auth.addUrlAuth('/api/users/' + id + '/')).then(
            function success(response) {
                $error.onSuccess('Пользователь успешно удален');
                $location.path('/clients/');
                $route.reload()
            },
            function error(response) {
                $error.onError(response);
            }
        )
    }
}
