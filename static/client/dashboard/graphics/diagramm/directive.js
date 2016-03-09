function reqWithPromise(url){
  return new Promise(function(resolve, reject) {
    jQuery.getJSON(url)
    .then(function(response){
      resolve(response);
    })
    .fail(function(err){
      reject(err);
    });
  });
};

function test(){
  var urls = ['user/1234/workouts'];

  urls.forEach(function(url){
    reqWithPromise(url)
    .then(function(res){
      console.log(url+' success: ', res);
    })
    .catch(function(){
      console.log(url+' failed request!');
    });
  });
};

test();

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

module.directive('diagramm', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/graphics/diagramm/tpl.html',
    controller: function ($scope, $element, $timeout) {
      console.log('diagramm');

      function plot(options){
        var config = {
          title:'Diagramm',
          interpolate: 'basic',
          chart_type: 'line',
          width: 600,
          height: 400,
          right: 40,
          target: '#diagramm-data-only',
          area: false,
          data: options.data,
          showPoints: true,
          showPointsData: options.points
        };

        MG.data_graphic(config);
      };

      User.getData()
      .then(function(data){
        //console.log('data', data, Object.keys(data).length);
        /*var set = _.slice(data, 1000, 1500);
        var fncStrs = ['exp(-x/25)*10', 'exp(-x/40)*10+5', 'exp(-x/40)*10-15'];
        var step = Math.floor(set.length/fncStrs.length);
        var subsets = _.map(fncStrs, function(filler, index){
          return _.slice(set, index*step, (index+1)*step);
        });
        var dataset = _.map(fncStrs, function(fnc, index){
          return interpolateRay(subsets[index], fnc);
        });

        plot({
          data: dataset,
          points: subsets
        });*/

        console.log(_.slice(data, 1000, 1500));
        MG.data_graphic({
            title: "Another Least Squares Example",
            description: "Least squares effortlessly works with dates or times on axes.",
            data: _.slice(data, 0, 100),
            chart_type: 'point',
            width: 600,
            height: 400,
            right: 40,
            least_squares: true,
            target: '#diagramm-data-only',
            //x_accessor: 'date',
            //y_accessor: 'value'
        });

        MG.data_graphic({
            title: "Another Least Squares Example",
            description: "Least squares effortlessly works with dates or times on axes.",
            data: _.slice(data, 0, 300),
            chart_type: 'point',
            width: 600,
            height: 400,
            right: 40,
            least_squares: true,
            target: '#diagramm-data-only1',
            //x_accessor: 'date',
            //y_accessor: 'value'
        });

        MG.data_graphic({
            title: "Another Least Squares Example",
            description: "Least squares effortlessly works with dates or times on axes.",
            data: _.slice(data, 200, 300),
            chart_type: 'point',
            width: 600,
            height: 400,
            right: 40,
            least_squares: true,
            target: '#diagramm-data-only2',
            //x_accessor: 'date',
            //y_accessor: 'value'
        });
      })
      .catch(function(err){
        console.log(err);
      });
    }
  };
});
