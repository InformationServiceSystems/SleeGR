module.directive('profile', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/profile/tpl.html',
    controller: function ($scope, $element, $timeout) {
      function getProfile(){
        User.getProfile()
        .then(function(user){
          $scope.user = user.profile;
          $scope.$apply();
        })
        .catch(console.log);
      };

      getProfile();

      /*$timeout(function(){
        getProfile();
      }, 3000);*/
    }
  };
});
