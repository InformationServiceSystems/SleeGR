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

function interpolateRay(set, funcStr){
  var ray = _.map(set, function(item, index){
    return { x: index, date: item.date };
  });

  var evaluate = createEvaluator(funcStr);
  var interpolate = createInterpolationOn(evaluate, function(scope, value){
    return {
      date: scope.date,
      value: value
    };
  });
  return interpolate(ray);
};

function formate(info){
  return moment(info, "YYYY.MM.DD_HH:mm:ss").toDate();
};

var DaysSeries = function(response){
  this.init(response);
};

DaysSeries.prototype.init = function(unstructured){
  this.structured = _.map(unstructured, function(item, str){
    return {
      date: formate(str),
      value: parseFloat(item.value)
    }
  });

  this.days = _.groupBy(this.structured, function(point){
    return moment(point.date).format("YYYY.MM.DD");
  });
};

DaysSeries.prototype.selectDays = function(dayKeys){
  var that = this;
  return _.reduce(dayKeys, function(allDays, key){
    return allDays.concat(that.days[key]);
  }, []);
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
  var id = 1024;
  var user;
  var workouts;
  var training;
  var measure;
  var heart;
  var csv;
  var dump;

  return {
    getDataset: function(start, end, sensor){
      var data;
      var path = '/show-stats/'+id+'/'+start+'/'+end+'/'+sensor;

      return new Promise(function(resolve, reject) {
        var container;
        if(container){
          resolve(container);
        } else {
          jQuery.getJSON(path)
          .then(function(response){
            data = new DaysSeries(response);
            //console.log(data.structured);
            //console.log(data.days);
            resolve(data);
          })
          .fail(function(err){
            console.log(err);
            reject(err);
          });
        }
      });

      /*return Service.get('/show-stats/1024/2016-01-01/2016-03-03/21', {
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

          var set = _.slice(dump, 1000, 1500);
          var fncStrs = ['exp(-x/25)*150+55', 'exp(-x/40)*150+50', 'exp(-x/40)*150+60'];
          var step = Math.floor(set.length/fncStrs.length);
          var subsets = _.map(fncStrs, function(filler, index){
            //return _.slice(set, index*step, set.length);
            return _.slice(set, index*step, (index+1)*step);
          });
          var dataset = _.map(fncStrs, function(fnc, index){
            return interpolateRay(_.slice(set, index*step, set.length), fnc);
          });

          var types = _.map(dataset, function(subset, index){
            return {
              type: index,
              data: subset,
              points: subsets[index]
            }
          });

          dump = types;

          return dump;
        }
      });*/
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
