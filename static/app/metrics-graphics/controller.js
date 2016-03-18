function MetricsGraphicsCtrl($scope, $element, $interval, PerformanceSlick) {
	var permform = new PerformanceAPI();
	$scope.target = $element.find('#metricsgraphics')[0];
	$scope.data = [];

	$scope.defaultGraphicOptions = {
		full_width: true,
		full_height: true,
		target: $scope.target,
		data: $scope.data
	};
	$scope.graphicOptions = {};

	$scope.graphic = function(options){
		//PerformanceSlick.perform('test');
		$scope.graphicOptions = angular.extend({}, $scope.extendGraphic(options));
		if($scope.graphicOptions.data.length > 0){
			MG.data_graphic($scope.graphicOptions);
		}
		//PerformanceSlick.perform('test');
	};

	$scope.extendGraphic = function(options){
		return angular.extend($scope.defaultGraphicOptions, options);
	};

	$scope.plot = function(data){
		if($scope.data.length === 0){
			$scope.data = data;
		}
		$scope.graphicOptions.data = data;
		MG.data_graphic($scope.graphicOptions);
	};

	$scope.addPoint = function(point){
		$scope.data.push(point);
		$scope.plot($scope.data);
	};

	$scope.addCollectionPoints = function(collection){
		$scope.data = $scope.data.concat(collection);
		$scope.plot($scope.data);
	};

	$scope.sequential = function(data){
		var add = function(){ $scope.addPoint(data.shift()); };
		$interval(add, 1000, data.length);
	};

	/*$timeout(function(){
		$scope.addPoint({
			"date": new Date("2015-09-09"),
			"value": 679569921
		});
	}, 2000);*/

	/*console.log('test');
	jQuery.getJSON('http://wiquation.net/json.php', function(json){
		console.log(json);
	}).fail(function(err) {
      console.log(err);
  });*/
}
