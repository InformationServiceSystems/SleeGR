function StocksResourceService ($resource) {
	//var url = 'https://www.quandl.com/api/v3/datasets/WIKI/:name.json';
	/*var Stocks = $resource('https://www.quandl.com/api/v3/datasets/WIKI/:name.json?start_date=2015-01-01&end_date=2015-09-01', {name: '@id'}, {
    _get: { method:'GET' }
  });

	Stocks.get = function(options){
		console.log(options);
		return Stocks._get(options);
	};

	return Stocks;*/
	return $resource('https://www.quandl.com/api/v3/datasets/WIKI/:name.json?start_date=2015-01-01&end_date=2015-09-01', {name: '@id'}, {
    'get': { method:'GET', cache: true}
  });
};
