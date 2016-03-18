function StocksSelectionCtrl ($scope, $element, Files) {
	document.addEventListener('deviceready', function () {
		jQuery('#info').html("connected to device ...");
		Files.download({
			url: "https://www.quandl.com/api/v3/datasets/WIKI/FB.csv",
			targetPath: cordova.file.dataDirectory + "test.csv",
			trustHosts: true,
			options: {}
		}, function(result) {
			jQuery('#info').html("download complete");
			//getFile();
		}, function(err) {
			jQuery('#info').html("error");
		}, function (progress) {
			// constant progress updates
			jQuery('#info').html("progress updates");
		});
	}, false);

	$scope.chart_types = ['line', 'point', 'bar', 'histogram'];
	$scope.chart_type = $scope.chart_types[0];
	$scope.setChartType = function(chart_type){
		$scope.graphic({chart_type: chart_type});

		if(chart_type == 'bar'){
			$scope.extend({
				bar_orientation: 'vertical'
			});
		}

		if(chart_type == 'histogram'){
			var second = d3.range(10000).map(function(d) { return Math.random() * 10; });
		  second = d3.layout.histogram()(second)
		    .map(function(d) {
		        return {'count': d.y, 'value': d.x};
		  });
			$scope.graphic({
		    data: second,
		    binned: true,
		    chart_type: 'histogram',
		    y_extended_ticks: true,
		    x_accessor: 'value',
		    y_accessor: 'count',
		    mouseover: function(d, i) {
		        d3.select('#histogram2 svg .mg-active-datapoint')
		            .text('Value: ' + d3.round(d.x,2) +  '   Count: ' + d.y);
		    }
		  });
		} else {
			//console.log($scope.graphicOptions, $scope.data);
			$scope.graphicOptions.data = $scope.data;
		}
		MG.data_graphic($scope.graphicOptions);
	};
};
