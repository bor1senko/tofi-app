angular.module("ui.bootstrap.core", ['ngAnimate', 'ngSanitize', 'ui.bootstrap']);
//module = angular.module("jupiter.core");
module.controller('HomeController', HomeController);

function HomeController($scope) {
    $scope.myInterval = 5000;
    $scope.noWrapSlides = false;
    $scope.active = 0;
    var slides = $scope.slides = [];
    var currIndex = 0;
    var slideItems = [
        {video: '/upload/iblock/d79/insync.mp4', text:'Улыбающаяся кукла'},
        {video: '/upload/iblock/5d8/banner_rentalcars.mp4', text:'Продал хату - купи тачку'},
        {video: '/upload/iblock/c98/booking.mp4', text:'Какая интересная карта'},
        {video: '/upload/iblock/2f7/credits.mp4', text:'Слоууумооо'}
    ]

    $scope.addSlide = function(slideItem) {
        slides.push({
          video: 'https://www.alfabank.by/' + slideItem.video,
          text: slideItem.text,
          id: currIndex++
        });
    };

    for (var i = 0; i < slideItems.length; i++) {
        $scope.addSlide(slideItems[i]);
    }
};
