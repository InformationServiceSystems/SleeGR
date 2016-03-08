var app = angular.module('sp', []);

app.directive('register', function () {
  return {
    restrict: 'E',
    templateUrl: 'smart-platform/js/registration/form.html',
    controller: function ($scope, $element) {
      $scope.message = 'Hello World!';
    }
  };
});
