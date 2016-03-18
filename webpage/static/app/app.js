var app = angular.module('insight', ['ngMaterial', 'ngResource', 'ngMessages', 'ngCordova']);

app.config(['$mdIconProvider', function($mdIconProvider) {
  $mdIconProvider
    //.iconSet('social', 'img/icons/sets/social-icons.svg', 24);
		//.icon('android', 'img/icons/sets/css/svg/sprite.css.svg');
    .iconSet('material', 'img/icons/sets/css/svg/sprite.css.svg');
}]);

app.factory('Files', ['$cordovaFile', '$cordovaFileTransfer', function($cordovaFile, $cordovaFileTransfer) {
	return FileSystem($cordovaFile, $cordovaFileTransfer);
}]);

app.factory('PerformanceSlick', PerformanceAPI);
app.factory('AppService', AppService);
app.controller('AppCtrl', AppCtrl);
app.controller('DatepickIntervalCtrl', DatepickIntervalCtrl);
app.directive('datepickInterval', DatepickIntervalDirective);
app.controller('DatepickSliderCtrl', DatepickSliderCtrl);
app.directive('datepickSlider', DatepickSliderDirective);
app.controller('MetricsGraphicsCtrl', MetricsGraphicsCtrl);
app.controller('MetricsGraphicsHistogramCtrl', MetricsGraphicsHistogramCtrl);
app.controller('StocksSelectionCtrl', StocksSelectionCtrl);
app.factory('Stocks', StocksResourceService);
app.directive('graphic', StocksMetricsGraphicsDirective);
app.directive('testHistogram', MetricsGraphicsHistogramDirective);
app.directive('metricsGraphics', MetricsGraphicsHistogramDirective);

//metrics graphics carousel
app.factory('MetricsGraphicsCarouselService', MetricsGraphicsCarouselService);
app.controller('MetricsGraphicsCarouselCtrl', MetricsGraphicsCarouselCtrl);
app.directive('metricsGraphicsCarousel', MetricsGraphicsCarouselDirective);

app.directive('testMetrics', function (Files) {
	return {
        restrict: 'E',
        template: '<div>loaded</div><div id="metricsgraphics" style="height: 80%; max-height: inherit;"></div>',
        controller: function ($scope, $element, $controller,  $interval, $timeout) {
					$controller('MetricsGraphicsCtrl', {
						$scope: $scope,
						$element: $element,
						$interval: $interval,
						$timeout: $timeout
					});

					jQuery.getJSON('http://wiquation.net/json.php', function(json){
						var rates = json.dataset.data.map(function(point){
							return {
								value: point[5],
								date: point[0]
							};
						//}).reverse();
						}).reverse().slice(0, 10);
						rates = MG.convert.date(rates, 'date');
						//alert(JSON.stringify(rates));
						$scope.plot(rates);
						$scope.$apply();
					}).fail(function(err) {
				    console.log('error', err);
				  });

					document.addEventListener('deviceready', function () {

					}, false);
	      }
    };
});

app.directive('hello', function (Files) {
	return {
        restrict: 'E',
        templateUrl: 'templates/hello.tpl.html',
        controller: function ($scope, $element) {
					//console.log($scope);
					$scope.json = {test: 'test'};

					document.addEventListener('deviceready', function () {
            alert('here');
						//jQuery('#info').html('connected to device!!!');
						/*Files.download({
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
						});*/
					}, false);

					/*function getFile(){
						$cordovaFile.checkFile(cordova.file.dataDirectory, "test.csv")
						.then(function (success) {
							jQuery('#info').html(JSON.stringify(success));

							$cordovaFile.readAsText(cordova.file.dataDirectory, "test.csv")
							.then(function (success) {
								jQuery('#info').html(JSON.stringify(success));
							}, function (error) {
								jQuery('#info').html("read file error!");
							});
						}, function (error) {
							jQuery('#info').html("error file check!");
						});
					};*/
	      },
	      link: function (scope, element) {

	      }
    };
});
