var module = angular.module('iss', []);

module.controller('navigation', ['$scope', function($scope) {
  $scope.mod = 'profile';

  $scope.render = function(name){
    $scope.mod = name;
    console.log(name);
  };
}]);

module.factory('User', function(){
  var user = {
    lastname: 'Sponge',
    firstname: 'Bob',
    email: 'Sponge.bob@gmail.com',
    height: 1.75,
    weight: 65,
    age: new Date(),
    gender: 'female'
  };

  var workouts = [{
    info: {
      date: '2016-02-08',
      time: '14:39'
    },
    data: [{
      value: 44,
      date: '2016-02-08'
    },{
      value: 27,
      date: '2016-02-09'
    },{
      value: 15,
      date: '2016-02-10'
    },{
      value: 9,
      date: '2016-02-11'
    },{
      value: 7,
      date: '2016-02-12'
    }]
  },{
    info: {
      date: '2016-02-14',
      time: '14:39'
    },
    data: [{
      value: 74,
      date: '2016-02-14'
    },{
      value: 27,
      date: '2016-02-15'
    },{
      value: 15,
      date: '2016-02-16'
    },{
      value: 14,
      date: '2016-02-17'
    },{
      value: 13,
      date: '2016-02-18'
    }]
  }];

  var training = {
    coach: {
      name: 'Blackbeard'
    },
    mates: [
      {
        name: 'Paul',
        score: {
          sessions: 20,
          success: 19
        }
      },
      {
        name: 'John',
        score: {
          sessions: 20,
          success: 13
        }
      }
    ]
  };

  var measure = {
    sleep: {
      data: [
        { year: '2008', value: 20 },
        { year: '2009', value: 10 },
        { year: '2010', value: 5 },
        { year: '2011', value: 5 },
        { year: '2012', value: 20 }
      ]
    }
  };

  return {
    getProfile: function(){
      return user;
    },
    getWorkouts: function(){
      return workouts;
    },
    getTraining: function(){
      return training;
    },
    getMeasure: function(name){
      return measure[name];
    }
  };
});

module.directive('profile', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/profile.tpl.html',
    controller: function ($scope, $element) {
      $scope.user = User.getProfile();
    }
  };
});

module.directive('workout', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/workout.tpl.html',
    controller: function ($scope, $element) {
      $scope.workouts =  User.getWorkouts();

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
      };

      $scope.chart($scope.workouts[0]['data']);
    }
  };
});

module.directive('measure', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/measure.tpl.html',
    controller: function ($scope, $element) {
      $scope.measurement = User.getMeasure('sleep');

      var measureChart = new Morris.Bar({
        // ID of the element in which to draw the chart.
        element: 'myfirstchart',
        // Chart data records -- each entry in this array corresponds to a point on
        // the chart.
        data: $scope.measurement.data,
        // The name of the data record attribute that contains x-values.
        xkey: 'year',
        // A list of names of data record attributes that contain y-values.
        ykeys: ['value'],
        // Labels for the ykeys -- will be displayed when you hover over the
        // chart.
        labels: ['Value']
      });

      /*setTimeout(function(){
        measureChart.setData([
          { year: '2009', value: 10 },
          { year: '2010', value: 5 },
          { year: '2011', value: 5 },
          { year: '2012', value: 20 }
        ]);
      }, 3000);*/
    }
  };
});

module.directive('training', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/training.tpl.html',
    controller: function ($scope, $element) {
      $scope.training = User.getTraining();
    }
  };
});
