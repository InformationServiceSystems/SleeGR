var StocksMetricsGraphicsDirective = function () {
	return {
		    restrict: 'E',
				scope: {name: '='},
        templateUrl: 'templates/stocks.tpl.html',
        controller: StocksMetricsGraphicsCtrl
    };
};
