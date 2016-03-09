module.directive('training', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/training/tpl.html',
    controller: function ($scope, $element, $timeout) {
      $scope.getTraining = function(){
        User.getTraining()
        .then(function(training){
          $scope.training = training;
          //console.log(training);
          $scope.$apply();
        })
        .catch(console.log);
      };

      $scope.getTraining();
    }
  };
});
