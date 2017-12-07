module = angular.module("jupiter.core");
module.controller('BaseController', BaseController);



function BaseController($error, $auth, $user, $scope, $timeout, $window) {
    $scope.user = $user;
    $scope.auth = $auth;
    $scope.error = $error;


    $scope.change_active_nav = function(index) {
        var elem = angular.element('.nav-link.active');
        elem.removeClass('active');
        if (index > 0) {
            var elem_id = "#nav-link-" + index;
            var elem = angular.element(elem_id);
            elem.addClass('active');
        }
    }


}