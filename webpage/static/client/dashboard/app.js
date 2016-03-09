var Service = {
  get: function(path, io){
    return new Promise(function(resolve, reject) {
      var container = io.get();
      if(container){
        resolve(container);
      } else {
        jQuery.getJSON(path)
        .then(function(response){
          io.set(response);
          resolve(io.get());
        })
        .fail(function(err){
          reject(err);
        });
      }
    });
  }
};

var module = angular.module('iss', ['ngMaterial']);

module.controller('navigation', ['$scope', function($scope) {
  $scope.mod = 'profile';

  $scope.render = function(name){
    $scope.mod = name;
    console.log(name);
  };
}]);

module.factory('User', function(){
  var id = 1234;
  var user;
  var workouts;
  var training;
  var measure;
  var heart;
  var csv;
  var dump;

  return {
    getData: function(){
      return Service.get('/show-stats/1024/2016-01-01/2016-03-03/21', {
        get: function(){
          return dump;
        },
        set: function(response){
          function formate(info){
            return moment(info, "YYYY.DD.MM_HH:mm:ss").toDate();
          };

          dump = _.map(response, function(item, str){
            return {
              date: formate(str),
              value: parseFloat(item.value)
            }
          });

          //console.log(dump);
          return dump;
        }
      });
    },
    getWorkouts: function(){
      return Service.get('user/'+id+'/workouts', {
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
      return Service.get('user/'+id+'/training', {
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
      return Service.get('user/'+id+'/measure', {
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
      return Service.get('user/'+id, {
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
      return Service.get('user/'+id+'/heartbeat', {
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
      return Service.get('user/'+id+'/csv', {
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
