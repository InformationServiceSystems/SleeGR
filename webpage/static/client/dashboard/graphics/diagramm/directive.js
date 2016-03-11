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


      $scope.removePoints = function(type){
        d3.select("#diagramm-data-only-showcase svg").selectAll(".mg-points-"+(type+1)).remove();
      };


      $scope.plotPoints = function(index){
        //console.log('plotPoints', index, $scope.cacheOptions.points[index], d3.select('#diagramm-data-only-showcase').select('svg'));
        var svg = d3.select('#diagramm-data-only-showcase').select('svg');
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

      $scope.exists = function (item, list) {
        return list.indexOf(item) > -1;
      };

      function plot(options){
        /*var config = {
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
        };*/

        var config = {
          title:'Diagramm',
          interpolate: 'basic',
          chart_type: 'point',
          width: 600,
          height: 400,
          right: 40,
          target: '#diagramm-data-only',
          area: false,
          data: options.data
        };

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

      $scope.items = [];
      $scope.selected = [];
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

      $scope.startDate = moment("2016-01-01", "YYYY-MM-DD").toDate();
      $scope.endDate = moment("2016-03-03", "YYYY-MM-DD").toDate();

      function formateDateToUrlSnipetAsString(date){
        return moment(date).format("YYYY-MM-DD");
      };

      $scope.series;
      $scope.days;

      $scope.draw = function(){
        plot({
          data: $scope.displayedPoints,
          points: $scope.displayedPoints,
          //selectorTypes: _.map(data, 'type')
        });

        //showcase state

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
      };

      $scope.setDays = function(days){
        $scope.days = days;
        $scope.displayedPoints = $scope.series.selectDays($scope.days);
        $scope.draw();
      };

      $scope.disabledDay = function(dateKey){
        return _.includes($scope.days, dateKey) === false;
      };

      $scope.toggleDay = function(dateKey){
        if(_.includes($scope.days, dateKey)){
          $scope.days = _.remove($scope.days, function(value){
            return value !== dateKey;
          });
        } else {
          $scope.days.push(dateKey);
        }
        $scope.setDays($scope.days);
      };

      $scope.switchDay = function(dateKey){
        $scope.setDays([dateKey]);
      };

      $scope.showAllDays = function(){
        $scope.setDays(_.keys($scope.series.days));
      };

      $scope.raised = function(dateKey){
        if(_.includes($scope.days, dateKey)){
          return 'md-raised';
        }
        return '';
      };

      $scope.getData = function(){
        var start = formateDateToUrlSnipetAsString($scope.startDate);
        var end   = formateDateToUrlSnipetAsString($scope.endDate);
        //console.log(start, end);

        User.getDataset(start, end, 21)
        .then(function(series){
          $scope.series = series;
          //$scope.setDays(['2016.02.05', '2016.02.27']);

          //$scope.setDays(_.keys($scope.series.days));

          var lastDayKey = _.last(_.keys($scope.series.days));
          $scope.setDays([lastDayKey]);

          $scope.draw();
          $scope.$apply();

          //showcase
          var data = $scope.series.selectDays(_.keys($scope.series.days));
          var set = _.slice(data, 1000, 1500);
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

          var showOptions = {
            data: _.map(types, 'data'),
            points: _.map(types, 'points'),
            selectorTypes: _.map(types, 'type')
          };

          $scope.cacheOptions = showOptions;

          var config = {
            title:'OLD Diagramm Prototype',
            interpolate: 'basic',
            chart_type: 'line',
            width: 600,
            height: 400,
            right: 40,
            target: '#diagramm-data-only-showcase',
            area: false,
            data: showOptions.data,
            showPoints: true,
            showPointsData: showOptions.points
          };

          $scope.graph = config;
          MG.data_graphic(config);

          $scope.items = showOptions.selectorTypes;
          $scope.selected = angular.copy(showOptions.selectorTypes);
          $scope.$apply();

          //test

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

      $scope.getData();
    }
  };
});
