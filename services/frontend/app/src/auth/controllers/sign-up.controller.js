module = angular.module("jupiter.auth");
module.controller('SignUpController', SignUpController);

// angular.module("jupiter.auth",['ngMaterial', 'ngMessages'] ).controller('AppCtrl', function() {
//   this.myDate = new Date();
//   this.isOpen = false;
// });

function SignUpController($auth, $error, $scope, $filter) {
    this.data = {
        username: "",
        password: "",
        email: "",
        profile: {},
        first_name: "",
        last_name: ""
    };

    this.myDate = new Date();
  this.isOpen = false;

    $scope.togglePassportExpiresPicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.passportExpiresPickerOpened = !$scope.passportExpiresPickerOpened;
    };

    this.signUp = function() {
        var passportExpires = this.data.profile.passport_expires;
        this.data.profile.passport_expires = $filter('date')(passportExpires, 'yyyy-MM-dd');

        var ctrl = this;
        $auth.signUp(
            this.data,
            function success() {
                $error.onSuccess(
                    'Спасибо. ' +
                    'Ваша заявка на регистрацию принята.' +
                    'После подтверждения вам на почту будет выслано уведомление.'
                );
            },
            function error(response) {
                ctrl.success = false;
                ctrl.errors = $error.prettifyErrors(response.data);
                $error.onError(response);
            }
        );
    };
}