/*function fake_data(length, seconds) {
    var d = new Date();
    var v = 100000;
    var data=[];

    for (var i = 0; i < length; i++){
        v += (Math.random() - 0.5) * 10000;
        data.push({date: MG.clone(d), value: v});
        d = new Date(d.getTime() + seconds * 1000);
    }
    console.log(data);
    return data;
}

function fake_days(length) {
    var d = new Date();
    var v = 100000;

    var data = [];
    for (var i = 0; i<length; i++) {
        v += (Math.random() - 0.5) * 10000;
        data.push({date: MG.clone(d), value: v});
        d.setDate(d.getDate() + 1);
    }
    return data;
}

var hist1 = fake_data(25, 60).map(function(d){
    d.value = Math.round(d.value);
    return d;
});

MG.data_graphic({
    title: "Histograms can be time series as well",
    data: hist1,
    target: '#time-hist',
    chart_type: 'histogram',
    width: 600,
    height: 200,
    binned: true,
});*/

var Service = {
  get: function(path, io){
    return new Promise(function(resolve, reject) {
      var container = io.get();
      if(container){
        resolve(container);
      } else {
        jQuery.getJSON(path)
        .then(function(response){
          container = response;
          io.set(container);
          resolve(container);
        })
        .fail(function(err){
          reject(err);
        });
      }
    });
  }
};

var module = angular.module('iss', []);

module.controller('navigation', ['$scope', function($scope) {
  $scope.mod = 'measure';

  $scope.render = function(name){
    $scope.mod = name;
    console.log(name);
  };
}]);

module.factory('User', function(){
  var user;
  var workouts;
  var training;
  var measure;
  var heart;
  var csv;

  return {
    getWorkouts: function(){
      return Service.get('user/1/workouts', {
        get: function(){
          return workouts;
        },
        set: function(response){
          workouts = response;
          return workouts;
        }
      });
    },
    getTraining: function(){
      return Service.get('user/1/training', {
        get: function(){
          return training;
        },
        set: function(response){
          training = response;
          return training;
        }
      });
    },
    getMeasure: function(name){
      //return measure[name];
      return Service.get('user/1/measure', {
        get: function(){
          return measure;
        },
        set: function(response){
          //console.log(response);
          measure = response;
          return measure;
        }
      });
    },
    getProfile: function(){
      return Service.get('user/1', {
        get: function(){
          return user;
        },
        set: function(data){
          data.profile.age = new Date(data.profile.age)
          user = data;
        }
      });
    },
    getHeartbeat: function(){
      return Service.get('user/1/heartbeat', {
        get: function(){
          return heart;
        },
        set: function(data){
          heart = _.map(data, function(row){
            row.date = new Date(row.date);
            return row;
          });
        }
      });
    },
    getCsv: function(){
      return Service.get('user/1/csv', {
        get: function(){
          return csv;
        },
        set: function(data){
          csv = [];

          _.forEach(data, function(container){
            csv.push(_.map(container, function(row){
              row.date = new Date(row.date);
              return row;
            }));
          });
        }
      });
    }
  };
});

module.directive('profile', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/profile.tpl.html',
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

module.directive('workout', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/workout.tpl.html',
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

module.directive('measure', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/measure.tpl.html',
    scope: {},
    controller: function ($scope, $element, $timeout) {
      /*jQuery(document).ready(function(){
        var mySlider = $("input.slider").bootstrapSlider();

        // Call a method on the slider
        var value = mySlider.bootstrapSlider('getValue');

        // For non-getter methods, you can chain together commands
        mySlider
            .bootstrapSlider('setValue', 5)
            .bootstrapSlider('setValue', 7);
      });*/

      $scope.chart = function(){
        var measureChart = new Morris.Bar({
          element: 'myfirstchart',
          data: $scope.measurement.data,
          xkey: 'year',
          ykeys: ['value'],
          labels: ['Value'],
          resize: true
        });
      };

      $scope.getMeasure = function(){
        User.getMeasure()
        .then(function(data){
          $scope.measurement = data.sleep;
          console.log($scope.measurement);
          $scope.$apply();
          //$scope.chart();
        })
        .catch(console.log);
      };

      $scope.getMeasure();
      //$scope.measurement = User.getMeasure('sleep');


      /*setTimeout(function(){
        measureChart.setData([
          { year: '2009', value: 10 },
          { year: '2010', value: 5 },
          { year: '2011', value: 5 },
          { year: '2012', value: 20 }
        ]);
      }, 3000);*/



      //heartbeat

      function scatter(data){
        MG.data_graphic({
            title: "Simple Line of Best Fit",
            description: "For any scatterplot.",
            data: data,
            least_squares: true,
            chart_type: 'point',
            width: 900,
            height: 400,
            right: 10,
            target: '#scatter-line-best-fit',
            xax_format: function(f) {
                var pf = d3.formatPrefix(f);
                return Math.round(pf.scale(f)) + pf.symbol;
            },
            x_accessor: 'date',
            y_accessor: 'value'
        });

        //console.log(theme);
        var color_range = 'light';
        MG.data_graphic({
          title: "Scatterplot with Size and Color",
          description: "Scatterplots have x_accessor, y_accessor, size_accessor, and color_accessor. For the last two you can also provide domain and range functions, to make it easy to change the color ranges. Colors default to red and blue, but can be overridden by passing an array of colors to color_range, as we've done in this example for the dark theme.",
          data: _.clone(data),
          chart_type: 'point',
          width: 900,
          height: 400,
          right: 10,
          target: '#scatter-size-and-color',
          xax_format: function(f) {
              var pf = d3.formatPrefix(f);
              return Math.round(pf.scale(f)) + pf.symbol;
          },
          x_accessor: 'date',
          y_accessor: 'value',
          color_accessor:'z',
          color_range: color_range,
          //size_accessor:'w',
          x_rug: true,
          y_rug: true
        });
      };

      $scope.options = {};
      $scope.store;
      $scope.intervall;

      $scope.setOptions = function(key, value){
        $scope.options[key] = value;
        plot($scope.store, $scope.intervall[0], $scope.intervall[1], $scope.options);
      };

      $scope.interpolate = function(value){
        $scope.options.interpolate = value;
        $scope.options.chart_type = undefined;
        plot($scope.store, $scope.intervall[0], $scope.intervall[1], $scope.options);
      };

      $scope.rug = function(axis){
        var key = axis+'_rug';
        $scope.options[key] = !$scope.options[key];
        console.log($scope.options);
        plot($scope.store, $scope.intervall[0], $scope.intervall[1], $scope.options);
      };

      $scope.plotFormula = false;
      $scope.plotMf = function(){
        $scope.plotFormula = !$scope.plotFormula;
        if($scope.plotFormula){
          $scope.options.mf = 'exp(-x/25)';
        } else {
          $scope.options.mf = undefined;
        }
        console.log();
        plot($scope.store, $scope.intervall[0], $scope.intervall[1], $scope.options);
      };

      function plot(data, start, end, options){
        var set = _.slice(data, start, end);
        scatter(set);

        var config = {
          title: "Small Range of Heartbeats",
          description: "When we have a data object of integers and a small range of values, the auto-generated set of y-axis ticks are filtered so that we don't include fractional values.",
          data: set,
          interpolate: 'basic',
          //chart_type: 'point',
          width: 900,
          height: 400,
          right: 40,
          target: '#heartbeat',
          animate_on_load: true,
          //y_extended_ticks: true,
          area: false,
          y_rug: true
          //x_rug: true
        }

        if(_.isUndefined(options) === false){
          if(options.chart_type){
            config.chart_type = options.chart_type;
          }
          if(_.isUndefined(options.y_rug) === false){
            config.y_rug = options.y_rug;
          }
          if(_.isUndefined(options.x_rug) === false){
            config.x_rug = options.x_rug;
          }
          if($scope.options.mf){
            config.mf = $scope.options.mf;
          }
        }

        //console.log(config.chart_type);
        //console.log('config', config.y_rug, config.x_rug);
        MG.data_graphic(config);
      };

      function createDistancer(min, max){
        var first, second;
        return function(intervall, movingLeft){
          first = intervall[0];
          second = intervall[1];
          if(second-first < min){
            return [first, first+min];
          }
          if(second-first > max){
            return [second-max, second];
          }
          return intervall;
        };
      };

      function directionLeft(event){
        var oldValue = event.value.oldValue;
        var newValue = event.value.newValue;
        //console.log(oldValue, newValue);
        if(oldValue[0] === newValue[0]){
          return true;
        }
        return false;
      };

      User.getHeartbeat()
      .then(function(data){
        var end = 1000;
        $scope.store = _.slice(data, 0, end);
        plot($scope.store, 0, end);

        jQuery(document).ready(function(){
          var slider = jQuery("#ex2").slider({
            min: 0,
            max: end,
            value: [0, end]
          });

          $scope.intervall = slider.slider('getValue');
          //slider.show();

          slider.on('change', function(event){
            $scope.intervall = slider.slider('getValue');
            plot($scope.store, $scope.intervall[0], $scope.intervall[1], $scope.options);
          });
        });
      })
      .catch(console.log);

      $timeout(function(){
        User.getCsv()
        .then(function(data){
          console.log(data);
          MG.data_graphic({
              title: "Multi-Line Chart",
              description: "This line chart contains multiple lines.",
              data: data,
              width: 900,
              height: 400,
              right: 40,
              target: '#fake_csv',
              legend: ['column 7','column 8'],
              //animate_on_load: true,
              //legend_target: '.legend'
          });
        })
        .catch(console.log);
      }, 500);
    }
  };
});

module.directive('training', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/training.tpl.html',
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
