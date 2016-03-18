function MetricsGraphicsHistogramCtrl ($scope, $element, $controller, $timeout, $interval) {
	$controller('MetricsGraphicsCtrl', {
		$scope: $scope,
		$element: $element,
		$interval: $interval,
		$timeout: $timeout
	});

	angular.extend($scope.graph, {
		chart_type: 'histogram',
		full_width: true,
		full_height: true,
		bins: 50,
    bar_margin: 0,
    target: '#histogram1',
    y_extended_ticks: true,
    mouseover: function(d, i) {
        d3.select('#histogram1 svg .mg-active-datapoint')
            .text('Value: ' + d3.round(d.x,2) +  '   Count: ' + d.y);
    }
	});

	$scope.plot(d3.range(10000).map(d3.random.bates(10)));
};
