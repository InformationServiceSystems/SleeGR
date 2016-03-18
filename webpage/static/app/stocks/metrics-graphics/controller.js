function StocksMetricsGraphicsCtrl ($scope, $element, $controller, $timeout, $interval, Stocks) {
	$controller('MetricsGraphicsCtrl', {
		$scope: $scope,
		$element: $element,
		$interval: $interval,
		$timeout: $timeout
	});

	angular.extend($scope.graphicOptions, {
		x_accessor: 'date',
		y_accessor: 'value',
	});

	$scope.get = function(name){
			Stocks.get({name: name}).$promise.then(function(response){
				plotStockRates(response.dataset.data);
			});
	};

	function plotStockRates(data){
		var rates = data.map(function(point){
			return {
				value: point[5],
				date: point[0]
			};
		//}).reverse();
		}).reverse().slice(0, 100);
		rates = MG.convert.date(rates, 'date');
		$scope.plot(rates);
		//$scope.sequential(rates);
	};

	//$scope.get('fb');
	//$scope.get('aapl');

	$scope.$watch('name', function(name, used) {
		if(angular.isDefined(name)){
			$scope.get(name);
		}
	});
	/*function get(){
		var deferred = Q.defer();
		jQuery.getJSON('/data', function(response){
			deferred.resolve(response);
		});
		return deferred.promise;
	};

	Q.fcall(get)
	.then(function(data){
		console.log(data);
	});*/
};
