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

//test();

module.directive('diagramm', function(User) {
  return {
    restrict: 'E',
    templateUrl: '/client/dashboard/graphics/diagramm/tpl.html',
    controller: function ($scope, $element, $timeout) {
      $scope.items = [];
      $scope.selected = [];
      $scope.toggle = function (item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) list.splice(idx, 1);
        else list.push(item);
      };
      $scope.exists = function (item, list) {
        return list.indexOf(item) > -1;
      };

      $scope.removePoints = function(type){
        d3.select("#diagramm-data-only svg").selectAll(".mg-points-"+(type+1)).remove();
      };

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
        var options = {
          data: _.map(data, 'data'),
          points: _.map(data, 'points'),
          selectorTypes: _.map(data, 'type')
        };

        plot(options);

        $scope.items = options.selectorTypes;
        $scope.$apply();


        //console.log(_.slice(data, 1000, 1500));
        /*MG.data_graphic({
            title: "Another Least Squares Example",
            description: "Least squares effortlessly works with dates or times on axes.",
            data: _.slice(data, 0, 100),
            chart_type: 'point',
            width: 600,
            height: 400,
            right: 40,
            least_squares: true,
            target: '#diagramm-data-only3',
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
        });*/
      })
      .catch(function(err){
        console.log(err);
      });
    }
  };
});
