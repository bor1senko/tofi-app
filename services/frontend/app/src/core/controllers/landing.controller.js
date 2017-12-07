angular.module("ui.bootstrap.core", ['ngAnimate', 'ngSanitize', 'ui.bootstrap']);
//module = angular.module("jupiter.core");
module.controller('HomeController', HomeController);

function HomeController($scope) {
    $scope.myInterval = 1000;
    $scope.noWrapSlides = false;
    $scope.active = 0;
    var slides = $scope.slides = [];
    var currIndex = 0;
    var slideItems = [
        {video: 'assets/img/email.icon.png', text:'telegram оповещения'},
        {video: 'http://activeinvestor.pro/wp-content/uploads/2014/08/kak-vybrat-vklad.jpg', text:'вклады'}
    ]

    $scope.addSlide = function(slideItem) {
        slides.push({
          video:  slideItem.video,
          text: slideItem.text,
          id: currIndex++
        });
    };

    for (var i = 0; i < slideItems.length; i++) {
        $scope.addSlide(slideItems[i]);
    }
};
