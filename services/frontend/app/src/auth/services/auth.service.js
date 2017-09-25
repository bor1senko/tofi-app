module = angular.module("jupiter.auth");
module.service("$auth", AuthService);


function AuthService($http, $url, $localStorage, $location) {
    var service = this;

    this.signIn = function(credentials, onSuccess, onError) {
        $http.post('/api/sign-in/', credentials).then(
            function success(response) {
                $localStorage.token = response.data.token;
                $localStorage.user = response.data.user;
                onSuccess(response);
                $location.path('/');
            },
            function error(response) {
               onError(response);
            }
        );
    };

    this.signOut = function(onSuccess, onError) {
        var token = $localStorage.token;
        if (token) {
            $http.get('api/sign-out/?token=' + token).then(
                function success(response) {
                    service._onSignOut();
                    if (onSuccess) {
                        onSuccess(response);
                    }
                },
                function error(response) {
                    service._onSignOut();
                    if (onError) {
                       onError(response);
                    }
                }
            )
        }
    };

    this.signUp = function(userData, onSuccess, onError) {
        $http.post('api/sign-up/', userData).then(
            function success(response) {
                $localStorage.token = response.data.token;
                onSuccess(response);
            },
            function error(response) {
                onError(response)
            }
        )
    };

    this.passwordReset = function(data, onSuccess, onError) {
        $http.post('api/password/reset/', data).then(
            function success(response) {
                onSuccess(response);
            },
            function error(response) {
                onError(response);
            }
        )
    };

    this.passwordResetConfirm = function(data, onSuccess, onError) {
        $http.post('api/password/confirm/', data).then(
            function success(response) {
                onSuccess(response);
            },
            function error(response) {
                onError(response);
            }
        )
    };

    this.addUrlAuth = function(url) {
        var token = $localStorage.token;
        return $url.query(url, 'token', token);
    };

    this._onSignOut = function() {
        delete $localStorage.token;
        delete $localStorage.user;
        $location.path("/");
    }
}
