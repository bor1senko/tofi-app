module = angular.module("jupiter.auth");
module.controller('PasswordResetController', PasswordResetController);


function PasswordResetController($auth, $error, $location) {
    this.reset_data = {
        email: ""
    };

    this.confirm_data = {
        key: "",
        new_password: "",
        new_password_confirm: ""
    };

    this.passwordReset = function() {
        var ctrl = this;
        ctrl.processing = true;
        $auth.passwordReset(
            this.reset_data,
            function success(response) {
                $location.path('/password-reset-confirm/');
                $error.clearErrors();
                ctrl.processing = false;
            },
            function error(response) {
                $error.onError(response);
                ctrl.processing = false;
            }
        );
    };

    this.passwordResetConfirm = function() {
        var ctrl = this;
        ctrl.processing = true;
        $auth.passwordResetConfirm(
            this.confirm_data,
            function success(response) {
                ctrl.processing = false;
                $location.path('/sign-in/');
                $error.clearErrors();
            },
            function error(response) {
                ctrl.processing = false;
                $error.onError(response);
            }
        );
    };
}
