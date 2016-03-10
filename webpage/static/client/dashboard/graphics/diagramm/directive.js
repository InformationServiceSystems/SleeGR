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

      $scope.removePoints = function(type){
        d3.select("#diagramm-data-only svg").selectAll(".mg-points-"+(type+1)).remove();
      };

      $scope.plotPoints = function(index){
        var svg = d3.select('#diagramm-data-only').select('svg');
        svg.selectAll("circle"+index)
         .data($scope.cacheOptions.points[index])
         .enter()
         .append("circle")
         .attr("cx", function(d) {
           return $scope.graph.scales.X(d.date);
         })
         .attr("cy", function(d) {
           return $scope.graph.scales.Y(d.value);
         })
         .attr("r", 1)
         .attr('class', 'mg-line mg-line'+(index+1)+' mg-line'+(index+1)+'-color mg-points-'+(index+1))
         //.style("stroke-width", 2)
         .style("fill", "none");
      };

      $scope.toggle = function (item, list) {
        var idx = list.indexOf(item);
        if (idx > -1) {
          $scope.removePoints(item);
          list.splice(idx, 1);
        } else {
          $scope.plotPoints(item);
          list.push(item);
        }
      };

      $scope.exists = function (item, list) {
        return list.indexOf(item) > -1;
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

        $scope.graph = config;
        MG.data_graphic(config);
      };

      function plotSleep(data){
        var config = {
          title: "Sleep",
          data: data,
          chart_type: 'point',
          width: 600,
          height: 400,
          right: 40,
          target: '#sleep',
          x_accessor: 'h',
          y_accessor: 'p',
          format: 'percentage',
          min_y: 0.3,
          max_y: 0.4
        };

        MG.data_graphic(config);

        try {
          //console.log(jQuery('#heatmap canvas')[0]);
          var heatmap = createWebGLHeatmap({canvas: jQuery('#heatmap canvas')[0]});
          var xStep = 600/11;
          var yStep = 10;
          var height = 350;
          _.map(data, function(item, index){
            heatmap.addPoint(item.h*xStep-50, 50+height-(0.4-item.p)/0.1*height, 35, 0.3);
          });
          //heatmap.multiply(0.995);
          //heatmap.clamp(0.0, 1.0);
          heatmap.update();
          heatmap.display();
          //heatmap.blur();
        } catch(error){
          console.log(error);
            // handle the error
        }
      };

      User.getData()
      .then(function(data){
        //console.log(data);
        var options = {
          data: _.map(data, 'data'),
          points: _.map(data, 'points'),
          selectorTypes: _.map(data, 'type')
        };

        $scope.cacheOptions = options;

        plot(options);

        function random(max){
          return Math.floor(max*Math.random());
        };

        function createSet(w, h, count){
          var set = [];
          for(var i=0; i<count; i += 1){
            set.push([random(w), random(h)]);
          }
          return set;
        };

        var sleep = [];
        _.forEach(createSet(12, 40, 1000), function(content){
          if(content[0] >= 2 && content[1] >= 30){
            sleep.push({
              h: content[0],
              p: content[1]/100
            });
          }
        });
        plotSleep(sleep);

        $scope.items = options.selectorTypes;
        $scope.selected = angular.copy(options.selectorTypes);
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
