module.directive('workout', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/workout/tpl.html',
    controller: function ($scope, $element) {
      $scope.chart = function(data){
        if(angular.isString(data[0]['date'])){
          MG.convert.date(data, 'date', '%Y-%m-%d');
        }

        MG.data_graphic({
          title: 'workout',
          description: "workouts of last month",
          data: data,
          full_width: true,
          target: document.getElementById('workout-chart'),
          x_accessor: 'date',
          y_accessor: 'value'
        });

        $scope.$apply();
      };

      $scope.getWorkouts = function(){
        User.getWorkouts()
        .then(function(workouts){
          $scope.workouts = workouts;
          $scope.chart($scope.workouts[0]['data']);
        })
        .catch(console.log);
      };

      $scope.getWorkouts();
    }
  };
});
